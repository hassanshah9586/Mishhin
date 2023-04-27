from odoo import api, models, fields, _, tools
import datetime
from dateutil.relativedelta import relativedelta
import tempfile
import os
import xlsxwriter


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    case_information_ids = fields.One2many(
        "case.information", "tenancy_id", string="Case Information"
    )
    judgement_date = fields.Datetime(
        string="judgement Date")
    judgement_details = fields.Text(
        string="Judgement")
    mandoob_id = fields.Many2one(
        "res.partner", string="Mandoob’s")
    legal_advisor_id = fields.Many2one(
        "res.partner", 
        string="Legal Advisor")
    operations_manager_id = fields.Many2one(
        "res.users",
        string="Operations Manager")
    type_id = fields.Many2one(
        comodel_name='property.type',
        string='Property Type',
        help='Types of property.',
        related='property_id.type_id',
        index=True)
    rent_amount_in_text = fields.Char(
        compute='_compute_check_amount_in_words',
        string='In Words',
        help="The amount in words")
    deposite_amount_in_text = fields.Char(
        compute='_compute_check_amount_in_words',
        string='Deosite In Words',
        help="The amount in words")

    @api.depends('currency_id', 'rent', 'tenant_id', 'deposit')
    def _compute_check_amount_in_words(self):
        for pay in self:
            if pay.currency_id:
                if pay.rent:
                    pay.rent_amount_in_text = pay.currency_id.with_context(lang=pay.tenant_id.parent_id.lang).amount_to_text(
                        pay.rent)
                else:
                    pay.rent_amount_in_text = False
                if pay.deposit:
                    pay.deposite_amount_in_text = pay.currency_id.with_context(lang=pay.tenant_id.parent_id.lang).amount_to_text(
                        pay.deposit)
                else:
                    pay.deposite_amount_in_text = False


class TenancyRentSchedule(models.Model):
    _inherit = "tenancy.rent.schedule"

    @api.model
    def send_non_payment_rent_email(self):
        email_context = dict(self._context) or {}
        template_rec_one_month = self.env.ref(
            "property_management_soor.send_one_month_warning_email"
        )
        current_date = datetime.date.today()
        last_3_month = current_date - relativedelta(months=3)
        last_2_month = current_date - relativedelta(months=2)
        last_month = current_date - relativedelta(months=1)
        email_context.update({"email_current_date": current_date})
        schedule_obj = self.env["tenancy.rent.schedule"]
        for rent in schedule_obj.search(
            [
                ("paid", "=", False),
                ("start_date", "in", [last_month, last_2_month, last_3_month]),
            ]
        ):
            manager_email = rent.tenancy_id.property_id.property_manager.email
            tenant_email = rent.tenancy_id.tenant_id.email
            legal_advisor_email = rent.legal_advisor_id.email or rent.property_id.legal_advisor_id.email
            emails = '%s, %s, %s' % (
                manager_email, tenant_email, legal_advisor_email),
            email_values = {'email_to': ','.join(emails)}
            # email_values = {"email_to": rent.tenancy_id.tenant_id.email}
            template_rec_one_month.with_context(email_context).send_mail(
                rent.id, email_values=email_values, force_send=True
            )
        return True
