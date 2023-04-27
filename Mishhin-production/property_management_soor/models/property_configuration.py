# See LICENSE file for full copyright and licensing details
from odoo import models, fields, _


class CaseType(models.Model):
    _name = "case.type"
    _description = "case Type"

    name = fields.Char(
        string='Name',
        required=True)
