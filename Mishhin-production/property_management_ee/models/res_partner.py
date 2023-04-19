# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    tenant = fields.Boolean(
        string='Tenant',
        help="Check this box if this contact is a tenant.")
    occupation = fields.Char(
        string='Occupation',
        size=20)
    agent = fields.Boolean(
        string='Agent',
        help="Check this box if this contact is a Agent.")
    mobile = fields.Char(
        string='Mobile',
        size=15)

    @api.model
    def default_get(self, fields_list):
        # company_id is added so that we are sure to fetch a default value from it to use in repartition lines, below
        values = super(ResPartner, self).default_get(fields_list)
        values['country_id'] = self.env['res.country'].search(
            [('code', '=', 'KW')], limit=1).id
        return values

    # def write(self, vals):
    #     res = super(ResPartner, self).write(vals)
    #     tenant_group = \
    #         self.env.ref('property_management_ee.group_property_user')
    #     agent_group = \
    #         self.env.ref('property_management_ee.group_property_agent')
    #     for partner in self:
            # if 'tenant' in vals:
            #     if not partner.tenant:
            #         if partner.user_ids.has_group(
            #                 'property_management_ee.group_property_user'):
            #             partner.user_ids.write(
            #                 {'groups_id': [(3, tenant_group.id)]})
            #     else:
            #         partner.user_ids.write(
            #             {'groups_id': [(4, tenant_group.id)]})
            # if 'agent' in vals:
            #     if not partner.agent:
            #         if partner.user_ids.has_group(
            #                 'property_management_ee.group_property_agent'):
            #             partner.user_ids.write(
            #                 {'groups_id': [(3, agent_group.id)]})
            #     else:
            #         partner.user_ids.write(
            #             {'groups_id': [(4, agent_group.id)]})
        # return res


class ResUsers(models.Model):
    _inherit = "res.users"

    tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Related Tenant')
    tenant_ids = fields.Many2many(
        comodel_name='tenant.partner',
        relation='rel_ten_user',
        column1='user_id',
        column2='tenant_id',
        string='All Tenants')


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_password = fields.Char(
        string='Default Password')
