from odoo import models, fields, _


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    bank_reference_id = fields.Many2one(
        'res.bank',
        string='Bank Refrence')
    check_reference = fields.Char(string='Check Reference')
    effective_date = fields.Date(
        'Effective Date', help='Effective date of Check', copy=False, default=False)
    journal_type = fields.Selection(string='type', related='journal_id.type', store=True)

    def _create_payment_vals_from_wizard(self):
        res = super()._create_payment_vals_from_wizard()
        res.update({'bank_reference_id': self.bank_reference_id.id,
                   'check_reference': self.check_reference, 'effective_date': self.effective_date})
        return res

class AccountPayment(models.Model):
    _inherit = "account.payment"

    bank_reference_id = fields.Many2one(
        'res.bank',
        string='Bank Refrence')
    check_reference = fields.Char(string='Check Reference')
    effective_date = fields.Date(
        'Effective Date', help='Effective date of Check', copy=False, default=False)
    journal_type = fields.Selection(string='type', related='journal_id.type', store=True)

