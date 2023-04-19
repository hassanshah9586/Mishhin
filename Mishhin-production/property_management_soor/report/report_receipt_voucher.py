# See LICENSE file for full copyright and licensing details
from odoo import models, api


class ReportreceiptVoucher(models.AbstractModel):
    _name = 'report.property_management_soor.report_receipt_voucher_details'
    _description = 'Property Rent Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        tenancy_ids = self.env['account.payment'].browse(docids)
        tenancy_ids = [tenancy_ids]
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.payment',
            'docs': tenancy_ids,
            'data': data,
            # 'get_amount': self.get_amount,
            # 'get_amount_due': self.get_amount_due,
        }
        return docargs
