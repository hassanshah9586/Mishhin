# See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import re

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    @api.onchange('user_id')
    def ochange_employee_id(self):
        for maintenance in self:
            maintenance.employee_id = self.env['hr.employee'].search([('user_id', '=', maintenance.user_id.id)], limit=1)

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'KW')],
                                                 limit=1).id
        return country


    property_id = fields.Many2one(
        string="Property Name",
        comodel_name="account.asset",
        help="Name of the property.")
    cost = fields.Float(
        string='Cost',
        default=0.0,
        help='Cost for over all maintenance')
    done = fields.Boolean(
        string='Stage Done',
        default=False)
    renters_fault = fields.Boolean(
        string='Renters Fault',
        default=False,
        copy=True,
        help='If this maintenance are fault by tenant than its true')
    invc_id = fields.Many2one(
        comodel_name='account.move', copy=False,
        string='Invoice')
    date_invoice = fields.Date(
        related="invc_id.invoice_date",
        store=True,
        string='Invoice Date')
    invc_check = fields.Boolean(
        string='Already Created',
        default=False)
    account_id = fields.Many2one(
        comodel_name='account.account',
        store=True,
        string='Maintenance Account')
    city = fields.Char(
        string='City',
        help='Enter the City')
    street = fields.Char(
        string='Street',
        help='Property street name')
    street2 = fields.Char(
        string='Street2',
        help='Property street2 name')
    township = fields.Char(
        string='Township',
        help='Property Township name')
    zip = fields.Char(
        related='property_id.zip',
        string='Zip',
        size=24,
        change_default=True,
        help='Property zip code')
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
        domain="[('country_id', '=', country_id)]",
        ondelete='restrict',
        help='Property state name')
    country_id = fields.Many2one(
        default=_get_default_country,
        comodel_name='res.country',
        string='Country',
        ondelete='restrict',
        help='Property country name')
    tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Tenant')
    is_in_progress = fields.Boolean(
        string='In Progress',
        default=False)
    payment_mode = fields.Selection(
        [("renters_fault", "Renters Fault"), ("petty_cash", "Petty Cash")], default='petty_cash')
    petty_cash_id = fields.Many2one(
        string="Petty cash holder",
        comodel_name="petty.cash",
        ondelete="restrict")
    attachment_number = fields.Integer(
        compute='_compute_attachment_number', string='Number of Attachments')
    sheet_id = fields.Many2one('maintenance.sheet', 'Sheet')

    # company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    # expance_state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('submit', 'Submitted'),
    #     ('approve', 'Approved'),
    #     ('post', 'Posted'),
    #     ('done', 'Paid'),
    #     ('cancel', 'Refused')
    # ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'maintenance.request'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count'])
                          for data in attachment_data)
        for maintenance in self:
            maintenance.attachment_number = attachment.get(maintenance.id, 0)

    def _prepare_expense_vals(self):
        vals = {
            "company_id": self.company_id.id,
            "employee_id": self.employee_id.id,
            "name": self.name if len(self) == 1 else "",
            "maintenance_line_ids": [(6, 0, self.ids)],
        }
        return vals

    def _create_sheet_from_expense_petty_cash(self):
        """ Overwrite function _create_sheet_from_expenses(), if petty cash mode. """
        if any(expense.sheet_id for expense in self):
            raise ValidationError(_("You cannot report twice the same line!"))
        if len(self.mapped("employee_id")) != 1:
            raise ValidationError(
                _(
                    "You cannot report expenses for different "
                    "employees in the same report."
                )
            )
        # if any(not expense.product_id for expense in self):
        #     raise ValidationError(_("You can not create report without product."))
        ctx = self._context.copy()
        ctx.update({"default_petty_cash_id": self[0].petty_cash_id.id})
        sheet = (
            self.env["maintenance.sheet"]
            .with_context(ctx)
            .create(self._prepare_expense_vals())
        )
        return sheet

    def _create_sheet_from_expenses(self):
        cash_vals = False
        payment_mode = set(self.mapped("payment_mode"))
        if len(payment_mode) > 1 and "petty_cash" in payment_mode:
            raise ValidationError(
                _("You cannot create report from many petty cash mode and other.")
            )
        if all(expense.payment_mode == "petty_cash" for expense in self):
            cash_vals = self._create_sheet_from_expense_petty_cash()
        return cash_vals
        # return super()._create_sheet_from_expenses()


    def action_submit_expenses(self):
        sheet = self._create_sheet_from_expenses()
        if sheet:
            return {
                'name': _('New Expense Report'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'maintenance.sheet',
                'target': 'current',
                'res_id': sheet.id,
            }
        else:
            pass

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id(
            'base.action_attachment')
        res['domain'] = [('res_model', '=', 'maintenance.request'),
                         ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'maintenance.request',
                          'default_res_id': self.id}
        return res

    @api.model
    def create(self, vals):
        request = super(MaintenanceRequest, self).create(vals)
        if vals.get('property_id') and not vals.get('tenant_id'):
            tenant_id = self.env['account.analytic.account'].search(
                [('property_id', '=', vals.get('property_id')),
                 ('is_property', '=', True),
                 ('state', '!=', 'close'),
                 ('state', '!=', 'cancelled')], limit=1).tenant_id
            if tenant_id:
                vals.update({'tenant_id': tenant_id.id})
        return request

    def open_google_map(self):
        """
        This Button method is used to open a URL
        according fields values.
        @param self: The object pointer
        """
        url = "http://maps.google.com/maps?oi=map&q="
        if self.property_id:
            for line in self.property_id:
                if line.name:
                    street_s = re.sub(r'[^\w]', ' ', line.name)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.street:
                    street_s = re.sub(r'[^\w]', ' ', line.street)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.street2:
                    street_s = re.sub(r'[^\w]', ' ', line.street2)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.township:
                    street_s = re.sub(r'[^\w]', ' ', line.township)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.city:
                    street_s = re.sub(r'[^\w]', ' ', line.city)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.state_id:
                    street_s = re.sub(r'[^\w]', ' ', line.state_id.name)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.country_id:
                    street_s = re.sub(r'[^\w]', ' ', line.country_id.name)
                    street_s = re.sub(' +', '+', street_s)
                    url += street_s + '+'
                if line.zip:
                    url += line.zip
            return {
                'name': 'Go to website',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'current',
                'url': url
            }

    @api.onchange('property_id')
    def state_details_change(self):
        for line in self:
            if line.property_id:
                line.tenant_id = self.env['account.analytic.account'].search(
                    [('property_id', '=', line.property_id.id),
                     ('is_property', '=', True),
                     ('state', '!=', 'close'),
                     ('state', '!=', 'cancelled')], limit=1).tenant_id
                line.street = line.property_id.street
                line.street = line.property_id.street2
                line.street = line.property_id.township
                line.street = line.property_id.city
                line.street = line.property_id.state_id
                line.street = line.property_id.country_id

            if line.property_id.maint_account_id:
                line.account_id = line.property_id.maint_account_id.id


    def write(self, vals):
        res = super(MaintenanceRequest, self).write(vals)
        for maintenance in self:
            if maintenance.stage_id.is_in_progress and 'stage_id' in vals:
                maintenance.write({'is_in_progress': True})
            if not maintenance.stage_id.is_in_progress and 'stage_id' in vals:
                maintenance.write({'is_in_progress': False})
            if maintenance.stage_id.done and 'stage_id' in vals:
                maintenance.write({'done': True})
        return res

    def create_invoice(self):
        """
        This Method is used to create invoice from maintenance record.
        --------------------------------------------------------------
        @param self: The object pointer
        """
        inv_line_values = []
        for data in self:
            if not data.property_id.id:
                raise ValidationError(_("Please Select Property"))
            tncy_ids = self.env['account.analytic.account'].search(
                [('property_id', '=', data.property_id.id), (
                    'state', '!=', 'close')])
            if len(tncy_ids.ids) == 0:
                inv_line_values.append((0, 0, {
                    'name': 'Maintenance For ' + data.name or "",
                    'ref': 'maintenance.request',
                    'quantity': 1,
                    'account_id': data.account_id.id or False,
                    'price_unit': data.cost or 0.00,
                }))
                inv_values = {
                    'invoice_origin': 'maintenance.request' or "",
                    'move_type': 'out_invoice',
                    'partner_id':
                    data.property_id.company_id.partner_id.id or False,
                    'property_id': data.property_id.id,
                    'invoice_line_ids': inv_line_values,
                    'amount_total': data.cost or 0.0,
                    'invoice_date': data.request_date or False,
                }

                acc_id = self.env['account.move'].with_context(
                    {'default_move_type': 'out_invoice'}).create(inv_values)
                data.write({'invc_check': True, 'invc_id': acc_id.id})
            else:
                inv_line_values.append((0, 0, {
                    'name': 'Maintenance For ' + data.name or "",
                    'ref': 'maintenance.request',
                    'quantity': 1,
                    'account_id': data.account_id.id or False,
                    'price_unit': data.cost or 0.00,
                }))
                for tenancy_data in tncy_ids:
                    inv_values = {
                        'invoice_origin': 'maintenance.request' or "",
                        'move_type': 'out_invoice',
                        'property_id': data.property_id.id,
                        'invoice_line_ids': inv_line_values,
                        'amount_total': data.cost or 0.0,
                        'invoice_date': data.request_date or False,
                        # 'number': tenancy_data.name or '',
                    }
                if data.payment_mode=='renters_fault':
                    inv_values.update({
                        'partner_id':
                        tenancy_data.tenant_id.parent_id.id or False})
                else:
                    inv_values.update(
                        {'partner_id':
                            tenancy_data.property_id.property_manager.id or
                            False})

                acc_id = self.env['account.move'].create(inv_values)
                data.write({
                    'invc_check': True,
                    'invc_id': acc_id.id,
                })

    def open_invoice(self):
        """
        This Method is used to Open invoice from maintenance record.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        wiz_form_id = self.env.ref('account.view_move_form').id
        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def _prepare_move_values(self):
        """
        This function prepares move values related to an expense
        """
        self.ensure_one()
        journal = self.sheet_id.journal_id
        account_date = self.sheet_id.accounting_date or fields.Date.context_today(self)
        move_values = {
            'journal_id': journal.id,
            'company_id': self.sheet_id.company_id.id,
            'date': account_date,
            'ref': self.sheet_id.name,
            # force the name to the default value, to avoid an eventual 'default_name' in the context
            # to set it to '' which cause no number to be given to the account.move when posted.
            'name': '/',
        }
        return move_values

    def _get_account_move_by_sheet(self):
        """ Return a mapping between the expense sheet of current expense and its account move
            :returns dict where key is a sheet id, and value is an account move record
        """
        move_grouped_by_sheet = {}
        for expense in self:
            # create the move that will contain the accounting entries
            if expense.sheet_id.id not in move_grouped_by_sheet:
                move_vals = expense._prepare_move_values()
                move = self.env['account.move'].with_context(
                    default_journal_id=move_vals['journal_id']).create(move_vals)
                move_grouped_by_sheet[expense.sheet_id.id] = move
            else:
                move = move_grouped_by_sheet[expense.sheet_id.id]
        return move_grouped_by_sheet

    def _get_expense_account_destination(self):
        self.ensure_one()
        account_dest = self.env['account.account']

        if not self.employee_id.sudo().address_home_id:
            raise UserError(_("No Home Address found for the employee %s, please configure one.") % (
                self.employee_id.name))
        partner = self.employee_id.sudo().address_home_id.with_company(self.company_id)
        account_dest = partner.property_account_payable_id.id or partner.parent_id.property_account_payable_id.id
        return account_dest

    def _get_expense_account_source(self):
        self.ensure_one()
        # if not self.account_id:
        #     raise UserError(
        #         _('Please configure Default Expense account for Maintenance Expense: `property_account_expense_categ_id`.'))
        account = self.account_id


        return account

    def _get_expense_account_destination(self):
        self.ensure_one()
        account_dest = self.env['account.account']
        if self.payment_mode == 'company_account':
            if not self.sheet_id.bank_journal_id.payment_credit_account_id:
                raise UserError(_("No Outstanding Payments Account found for the %s journal, please configure one.") % (
                    self.sheet_id.bank_journal_id.name))
            account_dest = self.sheet_id.bank_journal_id.payment_credit_account_id.id
        else:
            if not self.employee_id.sudo().address_home_id:
                raise UserError(_("No Home Address found for the employee %s, please configure one.") % (
                    self.employee_id.name))
            partner = self.employee_id.sudo().address_home_id.with_company(self.company_id)
            account_dest = partner.property_account_payable_id.id or partner.parent_id.property_account_payable_id.id
        return account_dest

    def _get_account_move_line_values(self):
        move_line_values_by_expense = {}
        for expense in self:
            move_line_name = expense.employee_id.name + \
                ': ' + expense.name.split('\n')[0][:64]
            account_src = expense._get_expense_account_source()
            account_dst = expense._get_expense_account_destination()
            account_date = expense.sheet_id.accounting_date or fields.Date.context_today(
                expense)

            move_line_values = []
            total_amount = 0.0
            partner_id = expense.employee_id.sudo().address_home_id.commercial_partner_id.id
            # source move line
            balance = expense.cost
            move_line_src = {
                'name': move_line_name,
                'quantity': 1,
                'debit': balance if balance > 0 else 0,
                'credit': -balance if balance < 0 else 0,
                'account_id': account_src.id,
                # 'analytic_account_id': expense.analytic_account_id.id,
                # 'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)],
                # 'expense_id': expense.id,
                'partner_id': partner_id,
                'currency_id': expense.currency_id.id,
            }
            move_line_values.append(move_line_src)
            total_amount -= balance
            # total_amount_currency -= move_line_src['amount_currency']
            # destination move line
            move_line_dst = {
                'name': move_line_name,
                'debit': total_amount > 0 and total_amount,
                'credit': total_amount < 0 and -total_amount,
                'account_id': expense.petty_cash_id.account_id.id,
                'date_maturity': account_date,
                'currency_id': expense.currency_id.id,
                # 'expense_id': expense.id,
                'partner_id': expense.petty_cash_id.partner_id.id,
            }
            move_line_values.append(move_line_dst)
            move_line_values_by_expense[expense.id] = move_line_values
        return move_line_values_by_expense

    def action_move_create(self):
        '''
        main function that is called when trying to create the accounting entries related to an expense
        '''
        move_group_by_sheet = self._get_account_move_by_sheet()
        move_line_values_by_expense = self._get_account_move_line_values()
        print('move_line_values_by_expense--------->',
              move_line_values_by_expense)
        for expense in self:
            # get the account move of the related sheet
            move = move_group_by_sheet[expense.sheet_id.id]
            # get move line values
            move_line_values = move_line_values_by_expense.get(expense.id)
            # link move lines to move, and move to expense sheet
            move.write({'line_ids': [(0, 0, line)
                       for line in move_line_values]})
            expense.sheet_id.write({'account_move_id': move.id})
        # post the moves
        for move in move_group_by_sheet.values():
            move._post()
        return move_group_by_sheet

class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    is_in_progress = fields.Boolean(
        string='In Progress',
        default=False)
