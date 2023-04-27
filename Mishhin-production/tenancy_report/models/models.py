# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words



class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def convert_amount_to_arabic(self, amm):
        return num2words(amm, lang ='ar') 1git st

    # amount_in_arabic = fields.Char(
    #     compute='_compute_check_amount_in_arabic',
    #     string='In Words',
    #     help="The amount in words")
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
    # @api.depends('rent')
    # def _compute_check_amount_in_arabic(self):
    #     for record in self:
    #         record.amount_in_arabic = record.convert_amount_to_arabic(record.rent)


