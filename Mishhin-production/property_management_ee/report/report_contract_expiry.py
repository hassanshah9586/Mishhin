# See LICENSE file for full copyright and licensing details
import time

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import ustr


class contract_expiry(models.AbstractModel):
    _name = 'report.property_management_ee.report_contract_expiry'
    _description = "Contract Expiry Report"

    def get_details(self, start_date, end_date):
        """
        This method is used to get the data from account analytic account
        between two dates.
        """
        data_1 = []
        tenancy_obj = self.env["account.analytic.account"]
        tenancy_ids = tenancy_obj.search(
            [('date', '>=', start_date),
             ('date', '<=', end_date),
             ('is_property', '=', True)])
        for data in tenancy_ids:
            if data.currency_id:
                cur = data.currency_id.symbol
            if data.date_start and data.date:
                user_lang = self.env.user.lang
                lang = self.env['res.lang'].search(
                    [('code', '=', user_lang)])
                start_date = data.date_start.strftime(lang.date_format)
                date = data.date.strftime(lang.date_format)
            data_1.append({
                'name': data.name,
                'property_id': data.property_id.name,
                'tenant_id': data.tenant_id.name,
                'date_start': start_date,
                'date': date,
                'rent': cur + ustr(data.rent),
                'rent_type_id': data.rent_type_id.name,
                'rent_type_month': data.rent_type_id.renttype,
                'state': data.state
            })
        return data_1

    def date_format(self, date):
        from_date = datetime.strptime(date, '%Y-%m-%d')
        user_lang = self.env.user.lang
        lang = self.env['res.lang'].search(
            [('code', '=', user_lang)])
        if from_date:
            final_from_date = from_date.strftime(lang.date_format)
        return final_from_date

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.asset'].browse(docids)
        start_date = data['form'].get('start_date', fields.Date.today())
        end_date = data['form'].get(
            'end_date', str(
                datetime.now() + relativedelta(
                    months=+1, day=1, days=-1))[:10])

        data_res = self.with_context(
            data['form'].get('used_context', {})).get_details(
                start_date, end_date)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.asset',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_details': data_res,
        }
        docargs['data'].update({
            'end_date': self.date_format(docargs.get('data').get('end_date')),
            'start_date': self.date_format(docargs.get('data').get(
                'start_date'))})
        return docargs
