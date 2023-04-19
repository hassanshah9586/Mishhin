# See LICENSE file for full copyright and licensing details

from odoo import models, fields

5.0

class TenantPaymentDetailsReport(models.TransientModel):
    _name = 'tenant.payment.details.report'
    _description = 'Tenant Payment Details Report'
    property_id = fields.Many2one(
        comodel_name='account.asset',
        string='Property',
        required=True)
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)

    def print_report(self):
        self.ensure_one()
        partner_obj = self.env['account.asset']
        for data_rec in self:
            data = data_rec.read([])[0]
            partner_rec = partner_obj.browse(data['property_id'][0])
            data.update({'property_name': partner_rec.name})
        return self.env.ref('property_management_soor.action_report_tenant_payment_details').report_action(None, data={'property_id': self.property_id.id,'start_date': self.start_date,'end_date': self.end_date,'form': data })
