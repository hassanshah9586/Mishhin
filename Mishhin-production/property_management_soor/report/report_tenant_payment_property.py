# See LICENSE file for full copyright and licensing details
from odoo import models, api, fields


class ReportPaymentProperty(models.AbstractModel):
    _name = 'report.property_management_soor.tenant_payment_property_id'
    _description = 'Report Tenant Payment Details'

    def get_details(self, start_date, end_date, property_id):
        final_dict = {}
        total_dict = {}
        tenancy_obj = self.env["tenancy.rent.schedule"]
        amount_rent_total = 0.0
        property_ids = self.env['account.asset'].browse(property_id)
        for rec in property_ids:
            tenancy_ids = tenancy_obj.search([
                ('tenancy_id.property_id', 'child_of', rec.id),
                ('tenancy_id.state', '=', 'open'),
                ('tenancy_id.rent_entry_chck', '=', True),
                ('start_date', '>=', start_date),
                ('start_date', '<=', end_date), ('paid', '!=', True)])
            for tenancy in tenancy_ids:
                tenancy_dict = {
                    'flat_no': tenancy.tenancy_id.property_id.flat_no,
                    'tenant_name': tenancy.tenancy_id.tenant_id.name,
                    'amount_due': tenancy.amount,
                    'receipt_no': tenancy.invc_id.name,
                }
                if rec in final_dict:
                    final_dict[rec].append(tenancy_dict)
                else:
                    final_dict.update({rec: [tenancy_dict]})
                amount_rent_total += tenancy.amount
            total_dict.update({rec: [amount_rent_total]})
        return [final_dict, total_dict]

    @api.model
    def _get_report_values(self, docids, data=None):
        # data['property_ids'] = data.get('property_ids', docids)
        detail_res = self.with_context(data['form'].get(
            'used_context', {})).get_details(
            data.get('start_date', docids), data.get('end_date', docids), data.get('property_ids', docids))
        date_from = fields.Date.from_string(data['start_date'])
        date_to = fields.Date.from_string(data['end_date'])
        docargs = {
            'doc_ids': docids,
            # 'docs': property_rec,
            'doc_model': 'account.asset',
            'date_start': date_from.strftime('%d-%m-%Y'),
            'date_end': date_to.strftime('%d-%m-%Y'),
            'get_details': detail_res,
        }
        return docargs
