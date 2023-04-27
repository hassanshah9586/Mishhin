# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    my_inv = fields.Many2one('account.move')

    def action_post(self):
        self.ensure_one()
        res = super(AccountMove, self).action_post()
        partners = []
        for line in self.invoice_line_ids:
            if line.product_id.partner_id.id not in partners:
                partners.append(line.product_id.partner_id.id)
            else:
                pass

        invoices_partner_wise_dict = {}
        for partner in partners:
            invoices_partner_wise_dict.update({partner: {'customer_invoices': [], 'vendor_bills': []}})

        for k, v in invoices_partner_wise_dict.items():
            for line in self.invoice_line_ids:
                if line.product_id.partner_id.id == k:
                    invoice_lines_vendor = []
                    invoice_lines_customer = []
                    # if line.product_id.commission_type == 'fixed':
                    if line.product_id.our_commission_fixe != 0:
                        product_line = (0, 0, {
                            'name': "Our Commission(" + str(
                                line.product_id.our_commission_fixe) + ") - " + line.product_id.name + "-" + self.name,
                            # 'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
                            'account_id': self.journal_id.default_account_id.id,
                            'quantity': '-1',
                            'price_unit': line.product_id.our_commission_fixe,
                            'price_subtotal': line.product_id.our_commission_fixe,
                        })
                        invoice_lines_vendor.append(product_line)

                    if line.product_id.fixed_commission != 0:
                        product_line = (0, 0, {
                            'name': line.product_id.name + "-" + self.name,
                            'account_id': line.account_id.id,
                            'quantity': '1',
                            'price_unit': line.product_id.fixed_commission,
                            'price_subtotal': line.product_id.fixed_commission,
                        })
                        invoice_lines_vendor.append(product_line)
                    if line.product_id.our_fixed_commission != 0:
                        product_line = (0, 0, {
                            'name': line.product_id.name + "-" + self.name,
                            'account_id': self.journal_id.default_account_id.id,
                            'quantity': '1',
                            'price_unit': line.product_id.our_fixed_commission,
                            'price_subtotal': line.product_id.our_fixed_commission,
                        })
                        invoice_lines_customer.append(product_line)
                    # if line.product_id.commission_type == 'percentage':
                    if line.product_id.our_commission_percent != 0:
                        if line.product_id.partner_id.id == k:
                            product_line = (0, 0, {
                                'name': "Our Commission(" + str(
                                    line.product_id.our_commission_percent) + ")% - " + line.product_id.name + "-" + self.name,
                                # 'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
                                'account_id': self.journal_id.default_account_id.id,
                                'quantity': '-1',
                                'price_unit': (line.price_subtotal * line.product_id.our_commission_percent) / 100,
                                'price_subtotal': (
                                                          line.price_subtotal * line.product_id.our_commission_percent) / 100,
                            })
                            invoice_lines_vendor.append(product_line)

                    if line.product_id.commission_percentage != 0:
                        if line.product_id.partner_id.id == k:
                            product_line = (0, 0, {
                                'name': line.product_id.name + "-" + self.name,
                                'account_id': line.account_id.id,
                                'quantity': '1',
                                'price_unit': (line.price_subtotal * line.product_id.commission_percentage) / 100,
                                'price_subtotal': (
                                                          line.price_subtotal * line.product_id.commission_percentage) / 100,
                            })
                            invoice_lines_vendor.append(product_line)
                    if line.product_id.our_commission_percentage != 0:
                        if line.product_id.partner_id.id == k:
                            product_line = (0, 0, {
                                'name': line.product_id.name + "-" + self.name,
                                'account_id': self.journal_id.default_account_id.id,
                                'quantity': '1',
                                'price_unit': (
                                                      line.price_subtotal * line.product_id.our_commission_percentage) / 100,
                                'price_subtotal': (
                                                          line.price_subtotal * line.product_id.our_commission_percentage) / 100,
                            })
                            invoice_lines_customer.append(product_line)
                    invoices_partner_wise_dict[k]['customer_invoices'].append(invoice_lines_customer)
                    invoices_partner_wise_dict[k]['vendor_bills'].append(invoice_lines_vendor)
        for k, v in invoices_partner_wise_dict.items():
            if invoices_partner_wise_dict[k]['customer_invoices']:
                invoice_lines = []
                for tup_list in invoices_partner_wise_dict[k]['customer_invoices']:
                    for tup in tup_list:
                        invoice_lines.append(tup)
                data = {
                    'partner_id': k if k else False,
                    'invoice_payment_term_id': 1,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': invoice_lines,
                    'my_inv':self.id,
                }
                if len(invoice_lines) == 0:
                    pass
                else:
                    inv = self.env['account.move'].sudo().create(data)
                    if inv:
                        for records in inv:
                            records.action_post()
            if invoices_partner_wise_dict[k]['vendor_bills']:
                invoice_lines = []
                for tup_list in invoices_partner_wise_dict[k]['vendor_bills']:
                    for tup in tup_list:
                        invoice_lines.append(tup)
                data = {
                    'partner_id': k if k else False,
                    'date': fields.Date.today(),
                    'invoice_date': fields.Date.today(),
                    'journal_id': self.env['account.journal'].search([('code', '=', 'BILL')]).id,
                    'invoice_payment_term_id': 1,
                    'move_type': 'in_invoice',
                    'invoice_line_ids': invoice_lines,
                    'my_inv': self.id,
                }
                if len(invoice_lines) == 0:
                    pass
                else:
                    bill = self.env['account.move'].sudo().create(data)
                    if bill:
                        for rec in bill:
                            rec.action_post()
        return res

    def action_view_invoices(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": 'tree,form',
            "name": "Invoices",
            # "context": {'default_box_id': self.id},
            "domain": [('my_inv', '=', self.id)]
        }

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Landlord")
    commission_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string="Type of Commission",
                                       default='fixed')
    commission_percentage = fields.Float(string="Commission %")
    fixed_commission = fields.Float(string="Fixed Commission")

    our_commission_percentage = fields.Float()
    our_fixed_commission = fields.Float()

    our_commission_percent = fields.Float(string="Our Commission %")
    our_commission_fixe = fields.Float(string="Our Fixed Commission")

    is_our_commission_readonly = fields.Boolean()
    is_our_comm_readonly = fields.Boolean()

    our_invoice_read = fields.Boolean(default=False)
    our_fixed_invoice_read = fields.Boolean(default=False)

    our_comp_read = fields.Boolean(default=False)
    our_fixed_comp_read = fields.Boolean(default=False)

    @api.onchange('our_commission_percentage')
    def set_readonly_fields_1(self):
        if self.our_commission_percentage > 0:
            self.our_invoice_read = False
            self.our_fixed_invoice_read = True
        else:
            self.our_invoice_read = False
            self.our_fixed_invoice_read = False

    @api.onchange('our_fixed_commission')
    def set_readonly_fields_2(self):
        if self.our_fixed_commission > 0:
            self.our_invoice_read = True
            self.our_fixed_invoice_read = False
        else:
            self.our_invoice_read = False
            self.our_fixed_invoice_read = False


    @api.onchange('our_commission_percent')
    def set_readonly_fields_3(self):
        if self.our_commission_percent > 0:
            self.our_comp_read = False
            self.our_fixed_comp_read = True
        else:
            self.our_comp_read = False
            self.our_fixed_comp_read = False

    @api.onchange('our_commission_fixe')
    def set_readonly_fields_4(self):
        if self.our_commission_fixe > 0:
            self.our_comp_read = True
            self.our_fixed_comp_read = False
        else:
            self.our_comp_read = False
            self.our_fixed_comp_read = False

    @api.onchange('our_commission_percentage', 'our_fixed_commission')
    def compute_is_commission_readonly(self):
        for rec in self:
            rec.is_our_commission_readonly = False
            rec.is_our_comm_readonly = False
            if rec.our_commission_percentage > 0 or rec.our_fixed_commission > 0:
                # rec.our_commission_percent = 0
                # rec.our_commission_fixe = 0
                rec.is_our_comm_readonly = True


    @api.onchange( 'our_commission_percent', 'our_commission_fixe')
    def compute_our_commission_readonly(self):
        for rec in self:
            rec.is_our_commission_readonly = False
            rec.is_our_comm_readonly = False
            if rec.our_commission_percent > 0 or rec.our_commission_fixe > 0:
                # rec.our_commission_percentage = 0
                # rec.our_fixed_commission = 0
                rec.is_our_commission_readonly = True

    @api.onchange('commission_type')
    def _setting_commission_values(self):
        self.ensure_one()
        if self.commission_type == 'fixed':
            self.commission_percentage = 0
            # self.our_commission_percentage = 0
            # self.our_commission_percent = 0
        elif self.commission_type == 'percentage':
            self.fixed_commission = 0
            # self.our_fixed_commission = 0
            # self.our_commission_fixe = 0
