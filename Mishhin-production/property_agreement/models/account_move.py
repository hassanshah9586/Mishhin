# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    my_inv = fields.Many2one('account.move')

    def action_view_invoices(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": 'tree,form',
            "name": "Invoices",
            # "context": {'default_box_id': self.id},
            "domain": [('my_inv', '=', self.id)]
        }

    def action_post(self):
        self.ensure_one()
        res = super(AccountMove, self).action_post()
        partners = self.property_id.partner_id.id
        # for line in self.invoice_line_ids:
        #     if line.product_id.partner_id.id not in partners:
        #         partners.append(line.product_id.partner_id.id)
        #     else:
        #         pass

        invoices_partner_wise_dict = {}
        # for partner in partners:
        invoices_partner_wise_dict.update({partners: {'customer_invoices': [], 'vendor_bills': []}})

        for k, v in invoices_partner_wise_dict.items():
            for line in self.invoice_line_ids:
                if self.property_id.partner_id.id == k:
                    invoice_lines_vendor = []
                    invoice_lines_customer = []
                    # if line.product_id.commission_type == 'fixed':
                    if self.property_id.our_commission_fixe != 0:
                        product_line = (0, 0, {
                            'name': "Our Commission(" + str(
                                self.property_id.our_commission_fixe) + ") - " + line.product_id.name + "-" + self.name,
                            # 'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
                            'account_id': self.journal_id.default_account_id.id,
                            'quantity': '-1',
                            'price_unit': self.property_id.our_commission_fixe,
                            'price_subtotal': self.property_id.our_commission_fixe,
                        })
                        invoice_lines_vendor.append(product_line)

                    if self.property_id.fixed_commission != 0:
                        product_line = (0, 0, {
                            'name': " ",
                            # 'name': line.product_id.name + "-" + self.name,
                            'account_id': line.account_id.id,
                            'quantity': '1',
                            'price_unit': self.property_id.fixed_commission,
                            'price_subtotal': self.property_id.fixed_commission,
                        })
                        invoice_lines_vendor.append(product_line)
                    if self.property_id.our_fixed_commission != 0:
                        product_line = (0, 0, {
                            'name': ' ',
                            # 'name': line.product_id.name + "-" + self.name,
                            'account_id': self.journal_id.default_account_id.id,
                            'quantity': '1',
                            'price_unit': self.property_id.our_fixed_commission,
                            'price_subtotal': self.property_id.our_fixed_commission,
                        })
                        invoice_lines_customer.append(product_line)
                    # if line.product_id.commission_type == 'percentage':
                    if self.property_id.our_commission_percent != 0:
                        if self.property_id.partner_id.id == k:
                            product_line = (0, 0, {
                                'name': "Our Commission(" + str(
                                    self.property_id.our_commission_percent) + ")% - " + line.product_id.name + "-" + self.name,
                                # 'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
                                'account_id': self.journal_id.default_account_id.id,
                                'quantity': '-1',
                                'price_unit': (line.price_subtotal * self.property_id.our_commission_percent) / 100,
                                'price_subtotal': (
                                                          line.price_subtotal * self.property_id.our_commission_percent) / 100,
                            })
                            invoice_lines_vendor.append(product_line)

                    if self.property_id.commission_percentage != 0:
                        if line.product_id.partner_id.id == k:
                            product_line = (0, 0, {
                                'name': ' ',
                                # 'name': line.product_id.name + "-" + self.name,
                                'account_id': line.account_id.id,
                                'quantity': '1',
                                'price_unit': (line.price_subtotal * self.property_id.commission_percentage) / 100,
                                'price_subtotal': (
                                                          line.price_subtotal * self.property_id.commission_percentage) / 100,
                            })
                            invoice_lines_vendor.append(product_line)
                    if self.property_id.our_commission_percentage != 0:
                        if self.property_id.partner_id.id == k:
                            product_line = (0, 0, {
                                # 'name': line.product_id.name + "-" + self.name,
                                'name': ' ',
                                'account_id': self.journal_id.default_account_id.id,
                                'quantity': '1',
                                'price_unit': (
                                                      line.price_subtotal * self.property_id.our_commission_percentage) / 100,
                                'price_subtotal': (
                                                          line.price_subtotal * self.property_id.our_commission_percentage) / 100,
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
                    'my_inv': self.id,
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
