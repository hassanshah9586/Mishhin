from odoo import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    electricity = fields.Boolean(string='Electricity Paid by Tenant or Not?')
    tenant_type = fields.Selection([
        ('individual', 'Individual'),
        ('company', 'Company'),
    ], string='Individual or Company')

    def action(self):
        for rec in self:
            rec.tenant_type = "individual"

