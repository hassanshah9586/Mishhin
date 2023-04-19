from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero
from odoo.tools import float_compare


class MaintenanceSheet(models.Model):
    _name = "maintenance.sheet"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Maintenance Report"
    _order = "accounting_date desc, id desc"
    _check_company_auto = True

    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    @api.model
    def _default_bank_journal_id(self):
        default_company_id = self.default_get(['company_id'])['company_id']
        return self.env['account.journal'].search([('type', 'in', ['cash', 'bank']), ('company_id', '=', default_company_id)], limit=1)

    @api.model
    def _default_journal_id(self):
        """ Update expense journal from petty cash """
        journal = False
        petty_cash_obj = self.env["petty.cash"]
        petty_cash = self._context.get("default_petty_cash_id", False)
        if petty_cash:
            petty_cash_id = petty_cash_obj.browse(petty_cash)
            journal = petty_cash_id.journal_id.id
        return journal

    name = fields.Char('Expense Report Summary', required=True, tracking=True)
    maintenance_line_ids = fields.One2many(
        'maintenance.request', 'sheet_id', string='Maintenance Lines', copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, tracking=True, states={'draft': [(
        'readonly', False)]}, default=_default_employee_id, check_company=True)
    address_id = fields.Many2one('res.partner', compute='_compute_from_employee_id', store=True,
                                 readonly=False, copy=True, string="Employee Home Address", check_company=True)
    payment_mode = fields.Selection([("petty_cash", "Petty Cash")],default='petty_cash', readonly=True, string="Paid By", tracking=True)
    user_id = fields.Many2one('res.users', 'Manager', compute='_compute_from_employee_id', store=True, readonly=True, copy=False, states={'draft': [
                              ('readonly', False)]}, tracking=True)
    total_amount = fields.Monetary(
        'Total Amount', currency_field='currency_id', compute='_compute_amount', store=True, tracking=True)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={
                                 'draft': [('readonly', False)]}, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={
                                  'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    attachment_number = fields.Integer(
        compute='_compute_attachment_number', string='Number of Attachments')
    journal_id = fields.Many2one('account.journal', string='Expense Journal', states={'done': [('readonly', True)], 'post': [('readonly', True)]}, check_company=True, domain="[('type', '=', 'purchase'), ('company_id', '=', company_id)]",
                                 default=_default_journal_id, help="The journal used when the expense is done.")
    bank_journal_id = fields.Many2one('account.journal', string='Bank Journal', states={'done': [('readonly', True)], 'post': [('readonly', True)]}, check_company=True, domain="[('type', 'in', ['cash', 'bank']), ('company_id', '=', company_id)]",
                                      default=_default_bank_journal_id, help="The payment method used when the expense is paid by the company.")
    accounting_date = fields.Date("Accounting Date")
    account_move_id = fields.Many2one(
        'account.move', string='Journal Entry', ondelete='restrict', copy=False, readonly=True)
    department_id = fields.Many2one('hr.department', compute='_compute_from_employee_id', store=True, readonly=False,
                                    copy=False, string='Department', states={'post': [('readonly', True)], 'done': [('readonly', True)]})
    can_reset = fields.Boolean('Can Reset', compute='_compute_can_reset')

    petty_cash_id = fields.Many2one(
        string="Petty cash holder",
        comodel_name="petty.cash",
        ondelete="restrict",
        compute="_compute_petty_cash",
    )

    _sql_constraints = [
        ('journal_id_required_posted', "CHECK((state IN ('post', 'done') AND journal_id IS NOT NULL) OR (state NOT IN ('post', 'done')))",
        'The journal must be set on posted expense'),
    ]

    @api.depends("maintenance_line_ids", "payment_mode")
    def _compute_petty_cash(self):
        for rec in self:
            rec.petty_cash_id = False
            if rec.payment_mode == "petty_cash":
                set_petty_cash_ids = set()
                for line in rec.maintenance_line_ids:
                    set_petty_cash_ids.add(line.petty_cash_id.id)
                if len(set_petty_cash_ids) == 1:
                    rec.petty_cash_id = rec.env["petty.cash"].browse(
                        set_petty_cash_ids.pop()
                    )
                else:
                    raise ValidationError(
                        _("You cannot create report from many petty cash holders.")
                    )

    @api.constrains("maintenance_line_ids", "total_amount")
    def _check_petty_cash_amount(self):
        for rec in self:
            if rec.payment_mode == "petty_cash":
                petty_cash = rec.petty_cash_id
                balance = petty_cash.petty_cash_balance
                print('balance------->', balance)
                amount = rec.total_amount
                print('amount-------->', amount)
                company_currency = rec.company_id.currency_id
                amount_company = rec.currency_id._convert(
                    amount,
                    company_currency,
                    rec.company_id,
                    rec.accounting_date or fields.Date.today(),
                )
                print("amount_company------->", amount_company)
                prec = rec.currency_id.rounding
                if float_compare(amount_company, balance, precision_rounding=prec) == 1:
                    raise ValidationError(
                        _(
                            "Not enough money in petty cash holder.\n"
                            "You are requesting %s%s, "
                            "but the balance is %s%s."
                        )
                        % (
                            "{:,.2f}".format(amount_company),
                            company_currency.symbol,
                            "{:,.2f}".format(balance),
                            company_currency.symbol,
                        )
                    )

    def unlink(self):
        for expense in self:
            if expense.state in ['post', 'done']:
                raise UserError(
                    _('You cannot delete a posted or paid expense.'))
        super(MaintenanceSheet, self).unlink()

    @api.depends('maintenance_line_ids.cost')
    def _compute_amount(self):
        for sheet in self:
            sheet.total_amount = sum(
                sheet.maintenance_line_ids.mapped('cost'))

    def _compute_attachment_number(self):
        for sheet in self:
            sheet.attachment_number = sum(
                sheet.maintenance_line_ids.mapped('attachment_number'))

    def _compute_can_reset(self):
        is_expense_user = self.user_has_groups(
            'property_maintenance_ee.group_maintenance_team_approver')
        for sheet in self:
            sheet.can_reset = is_expense_user if is_expense_user else sheet.employee_id.user_id == self.env.user

    @api.depends('employee_id')
    def _compute_from_employee_id(self):
        for sheet in self:
            sheet.address_id = sheet.employee_id.sudo().address_home_id
            sheet.department_id = sheet.employee_id.department_id
            sheet.user_id = sheet.employee_id.parent_id.user_id

    def action_submit_sheet(self):
        self.write({'state': 'submit'})

    def approve_expense_sheets(self):
        if not self.user_has_groups('property_maintenance_ee.group_maintenance_team_approver'):
            raise UserError(
                _("Only Managers and HR Officers can approve expenses"))
        elif not self.user_has_groups('property_maintenance_ee.group_maintenance_sheet_manager'):
            current_managers = self.employee_id.expense_manager_id | self.employee_id.parent_id.user_id | self.employee_id.department_id.manager_id.user_id

            if self.employee_id.user_id == self.env.user:
                raise UserError(_("You cannot approve your own expenses"))

            if not self.env.user in current_managers and not self.user_has_groups('property_maintenance_ee.group_maintenance_sheet_manager') and self.employee_id.expense_manager_id != self.env.user:
                raise UserError(
                    _("You can only approve your department expenses"))

        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('There are no Maintenance reports to approve.'),
                'type': 'warning',
                'sticky': False,  # True/False will display for few seconds if false
            },
        }
        filtered_sheet = self.filtered(
            lambda s: s.state in ['submit', 'draft'])
        if not filtered_sheet:
            return notification
        for sheet in filtered_sheet:
            sheet.write(
                {'state': 'approve', 'user_id': sheet.user_id.id or self.env.user.id})
        notification['params'].update({
            'title': _('The expense reports were successfully approved.'),
            'type': 'success',
            'next': {'type': 'ir.actions.act_window_close'},
        })

        return notification

    def action_sheet_move_create(self):
        if any(sheet.state != 'approve' for sheet in self):
            raise UserError(
                _("You can only generate accounting entry for approved expense(s)."))

        if any(not sheet.journal_id for sheet in self):
            raise UserError(
                _("Expenses must have an expense journal specified to generate accounting entries."))

        maintenance_line_ids = self.mapped('maintenance_line_ids')\
            .filtered(lambda r: not float_is_zero(r.cost, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
        res = maintenance_line_ids.action_move_create()
        for sheet in self.filtered(lambda s: not s.accounting_date):
            sheet.accounting_date = sheet.account_move_id.date
        self.write({'state': 'done'})
        return res

    def reset_expense_sheets(self):
        if not self.can_reset:
            raise UserError(_("Only HR Officers or the concerned employee can reset to draft."))
        # self.mapped('maintenance_line_ids').write({'is_refused': False})
        self.write({'state': 'draft'})
        return True
