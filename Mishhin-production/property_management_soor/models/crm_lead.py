from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
import string
import secrets
import datetime
from dateutil.relativedelta import relativedelta

DOCUMENT_TYPE = {
        'civil_id': 'Civil ID',
        'passport_copy': 'Passport Copy',
        'work_permit': 'Work Permit',
        'salary_certificate': 'Salary Certificate',
        'marriage_certificate': 'Marriage Certificate',
        'annual_income': 'Annual Income – Required by Law',
        'company_licence': 'Company License',
        'company_registration': 'Company registration',
        'articale_of_asociation': 'Articles of Association',
        'annual_company_income': 'Annual Company Income'
}


class CrmStage(models.Model):
    _inherit = "crm.stage"

    is_varification = fields.Boolean(string='Is Varification Stage ?')

    @api.constrains('is_varification')
    def check_is_varification(self):
        for rec in self:
            if rec.search([('is_varification', '=', True),
                            ('id', '!=', rec.id)], limit=1):
                raise ValidationError(
                    _("You can not have more than one Varification stage!"))
        return True


class CrmLead(models.Model):
    _inherit = "crm.lead"

    lead_attachment_ids = fields.One2many('lead.attachment', 'crm_id', string='Lead attachment')
    lead_token = fields.Char(string='Lead Token', readonly=True)
    in_varification = fields.Boolean(compute='get_is_varification', string='In Varification', store=True)
    expiry_date = fields.Date(
        string='Expiry Date')
    civil_id = fields.Char(string='Civil ID')
    annual_company_income = fields.Char(string='Annual Company Income')


    def action_set_won(self):
        case = self
        if case.lead_attachment_ids and case.lead_attachment_ids.filtered(lambda r: r.state != 'approved'):
            raise ValidationError(
                _('Some of document are not in approved in Applicant Document!'))
        return super(CrmLead, self).action_set_won()

    @api.depends('stage_id')
    def get_is_varification(self):
        current_date = datetime.date.today()
        company = self.env.company
        for rec in self:
            if rec.stage_id and rec.stage_id.is_varification:
                rec.in_varification = True
                rec.expiry_date = current_date + \
                    relativedelta(days=company.lead_expired_day)
            else:
                rec.in_varification = False

    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        res.lead_token = res._get_default_token()
        email_values = {"email_to": res.email_from}
        template_rec = self.env.ref("property_management_soor.send_token_genrated_email")
        template_rec.with_context({'token_key': res.lead_token}).send_mail(res.id, email_values=email_values, force_send=True)
        return res

    # @api.constrains('stage_id','in_varification')
    # def check_in_varification(self):
    #     for rec in self:
    #         if rec.in_varification and rec.lead_attachment_ids.filtered(lambda r: r.state not in ['approved','draft']):
    #             raise ValidationError(
    #                 _("Some of document are not in approved in Applicant Document!"))
    #     return True

    def _get_default_token(self):
        def generate_token(N=8):
            res = "".join(
                secrets.choice(string.ascii_uppercase + string.digits) for i in range(N)
            )
            exist = self.search([("lead_token", "=", res)], limit=1)
            if exist:
                res = generate_token(8)
            return res

        token = generate_token(8)
        return token

    @api.model
    def send_rejected_mail_upload_email(self):
        current_date = datetime.date.today()
        company = self.env.company
        # expiry_date = current_date - relativedelta(days=company.pending_attachment_reminder)
        expiry_date = current_date + relativedelta(days=company.pending_attachment_reminder)
        lead_ids = self.env['crm.lead'].search([('in_varification','=',True), ('expiry_date','=', expiry_date)])
        for lead in lead_ids:
            ctx = []
            email_values = {"email_to": lead.email_from}
            for document in lead.lead_attachment_ids.filtered(lambda r: r.state not in ['rejected', 'draft']):
                ctx.append(DOCUMENT_TYPE.get(document.document_type))

            template_rec = self.env.ref("property_management_soor.send_wrong_document_upload_warning_email")
            template_rec.with_context({'document_list': ctx}).send_mail(lead.id, email_values=email_values, force_send=True)

        return True

class LeadAttachment(models.Model):
    _name = 'lead.attachment'
    _description = 'Lead Attachment'

    doc_name = fields.Char(
        string='Filename')
    expiry_date = fields.Date(
        string='Expiry Date')
    contract_attachment = fields.Binary(
        string='Attachment')
    description = fields.Char(
        string='Description',
        size=64)
    crm_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Crm')
    document_type = fields.Selection([
        ('civil_id', 'Civil ID'),
        ('passport_copy', 'Passport Copy'),
        ('work_permit', 'Work Permit'),
        ('salary_certificate', 'Salary Certificate'),
        ('marriage_certificate', 'Marriage Certificate'),
        ('annual_income', 'Annual Income – Required by Law'),
        ('company_licence', 'Company License'),
        ('company_registration', 'Company registration'),
        ('articale_of_asociation', 'Articles of Association'),
        ('annual_company_income', 'Annual Company Income')
        ], string='Document Type', required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('approved', 'Approved'),
        ('re_review', 'RE-Review'),
        ('rejected', 'Rejected')
    ], string='Document approvel', default='draft')
    tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Tenant')


class CrmMakeContract(models.TransientModel):
    _inherit = "crm.make.contract"
    _description = "Make sales"

    def makecontract(self):
        context = dict(self._context or {})
        data = context and context.get('active_ids', []) or []
        lead_obj = self.env['crm.lead']
        for case in lead_obj.browse(data):
            if case.lead_attachment_ids and case.lead_attachment_ids.filtered(lambda r: r.state != 'approved'):
                raise ValidationError(
                    _('Some of document are not in approved in Applicant Document!'))
        return super().makecontract()
