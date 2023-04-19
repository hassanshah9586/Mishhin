# See LICENSE file for full copyright and licensing details
from odoo import models, fields, _


class CaseInformation(models.Model):
    _name = "case.information"
    _description = "Case Information"
    _rec_name = 'case_number'

    tenancy_id = fields.Many2one(
        'account.analytic.account',
        string='Tenancy')
    tenant_id = fields.Many2one(
        'tenant.partner',
        related='tenancy_id.tenant_id',
        store=True,
        string='Partner')
    case_type_id = fields.Many2one(
        'case.type',
        string='Case Type')
    lawyer_office = fields.Many2one(
        'res.partner',
        string='lawyer Office')
    case_number = fields.Char(
        string='Case Number')
    electronic_case_number = fields.Char(
        string='Electronic Case Number')
    date_of_lawsuit = fields.Datetime(
        string='Date oflawsuit')
    judgement_details = fields.Text(string='Judgement')
    judgement_date = fields.Date(string='Judgement Date')
    line_ids = fields.One2many(
        'case.information.line', 'case_information_id', string='Case Line')
    attachment_ids = fields.One2many(
        'legal.attachment',
        'case_information_id',
        string='Attachment')
    active = fields.Boolean(
        'Active', default=True,
        help="By unchecking the active field, you may hide an INCOTERM you will not use.")


class CaseInformationLine(models.Model):
    _name = "case.information.line"
    _description = "Case Information Line"

    name = fields.Char(
        string='Description',
        required=True)
    date = fields.Datetime(
        string='Date')
    next_session_date = fields.Datetime(
        string='Next Session Date')
    case_information_id = fields.Many2one(
        'case.information',
        string='Case')
    doc_name = fields.Char(
        string='Filename')
    id_attachment = fields.Binary(
        string='Identity Proof')


class LegalAttachment(models.Model):
    _name = 'legal.attachment'
    _description = 'Legal Attachment'

    doc_name = fields.Char(
        string='Filename')
    contract_attachment = fields.Binary(
        string='Attachment')
    name = fields.Char(
        string='Description',
        size=64,
        translate=True,
        required=True)
    case_information_id = fields.Many2one(
        'case.information',
        string='Case')
