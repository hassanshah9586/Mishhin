# See LICENSE file for full copyright and licensing details
from odoo import models, fields


class TenantPaymentPropertyReport(models.TransientModel):
    _name = 'tenant.payment.property.report'
    _description = 'Tenant Payment Property Report'

    property_ids = fields.Many2many(
        comodel_name='account.asset',
        string='Property',
        required=True)
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)

    # def print_report(self):
    #     self.ensure_one()
    #     return self.env.ref('property_management_soor.').report_action(None, data={'property_ids': self.property_ids.ids, 'start_date': self.start_date, 'end_date': self.end_date})

    def print_report(self):
        self.ensure_one()
        partner_obj = self.env['account.asset']
        for data_rec in self:
            data = data_rec.read([])[0]
            # partner_rec = partner_obj.browse(data['property_ids'][0])
            # data.update({'property_name': partner_rec})
        return self.env.ref('property_management_soor.action_tenant_payment_property_id').report_action(None, data={
            'property_ids': self.property_ids.ids, 'start_date': self.start_date, 'end_date': self.end_date, 'form': data})
