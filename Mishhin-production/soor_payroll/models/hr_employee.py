from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    nationality_child = fields.Many2one(
        'res.country',
        'Nationality of Children',
        groups="hr.group_hr_user",
        tracking=True)
    certificate = fields.Selection(
        selection_add=[
            ('high', 'High(Master/Doctoral)'),
            ('special', 'Special'),
            ('professional', 'Professional')
            ])
