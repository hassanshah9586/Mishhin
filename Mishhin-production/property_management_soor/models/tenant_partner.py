from odoo import models, fields, _


class AccountAnalyticAccount(models.Model):
    _inherit = "tenant.partner"

    case_information_ids = fields.One2many(
        'case.information',
        'tenant_id',
        string='Case Information')
    civil_id = fields.Char('Civil ID')
    nationality = fields.Many2one('res.country', 'Nationality')
    lead_attachment_ids = fields.One2many(
        'lead.attachment', 'tenant_id', string='Lead attachment')
