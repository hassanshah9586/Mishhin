from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    company = fields.Selection([
        ('company1', 'Mashhin Kuwaiti Real Estate Co.W.L.L.'),
        ('company2', 'Auto Capital for Selling and Buying and Leasing Cars Co.W.L.L.'),
        ('company3', 'Mustafa Thunayan AlGhanim & Partners Co.'),
        ('company4', 'AlMuhallab Building Construction Company'),
    ], string='Company')
