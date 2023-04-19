# See LICENSE file for full copyright and licensing details
from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = "res.company"

    fax = fields.Char('Fax')
    commercial_record = fields.Char('Commercial Record')
    pending_attachment_reminder = fields.Integer(
        string="Pending Attachment Reminder(Day's)", required=True, default=2)
    lead_expired_day = fields.Integer(string="Lead Expiry Date' Days(From Varification)", default=7)
    copyright_dev = fields.Char('Copyright')
