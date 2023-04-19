# See LICENSE file for full copyright and licensing details
from odoo import models, api, fields


class ReportPaymentDetails(models.AbstractModel):
    _name = 'report.property_management_soor.report_tenant_payment_details'
    _description = 'Report Tenant Payment Details'

    def get_details(self, start_date, end_date, property_id):
        tenancy_obj = self.env["tenancy.rent.schedule"]
        tenancy_ids = tenancy_obj.search([
            ('tenancy_id.property_id', 'child_of', property_id),
            ('tenancy_id.state', '=', 'open'),
            ('tenancy_id.rent_entry_chck', '=', True),
            ('start_date', '>=', start_date),
            ('start_date', '<=', end_date), ('paid', '!=', True)])
        print(len(tenancy_ids),'tennnnnnnnnnnnnnnnnnnnnnnnnnnn')
        return tenancy_ids

    @api.model
    def _get_report_values(self, docids, data=None):
        # data['property_id'] = data.get('property_id', docids)
        # data['start_date'] = data.get('start_date', docids)
        # data['end_date'] = data.get('end_date', docids)
        detail_res = self.with_context(data['form'].get(
            'used_context', {})).get_details(
            data.get('start_date', docids), data.get('end_date', docids), data.get('property_id', docids))
        print(len(detail_res),'--------------------')

        property_rec = self.env['account.asset'].browse(data['property_id'])
        sub_property = self.env['account.analytic.account'].search(
            [('property_id', 'child_of', property_rec.id), ('state', '=', 'open')])
        date_from = fields.Date.from_string(data['start_date'])
        date_to = fields.Date.from_string(data['end_date'])
        for rec in detail_res:
            print('name',rec.tenancy_id.tenant_id.name)
        print('ttttttttttttttttttt', len(detail_res))
        docargs = {
            'docs': property_rec,
            # 'doc_model': 'account.payment',
            'tenancy_ids': sub_property,
            'date_start': date_from.strftime('%d-%m-%Y'),
            'date_end': date_to.strftime('%d-%m-%Y'),
            'data': data,
            'get_details': detail_res,
            # 'get_amount_due': self.get_amount_due,
        }
        return docargs
