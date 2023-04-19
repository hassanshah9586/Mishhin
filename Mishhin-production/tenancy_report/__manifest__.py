# -*- coding: utf-8 -*-
{
    'name': "tenancy_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check httptemplatess://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/monthly_contract_ind_mish.xml',
        'views/month_contract_6.xml',
        'views/month_contract_6_ind.xml',
        'views/monthly_contract_companies.xml',
        # 'views/monthly_contract_ind_mish.xml',
        'views/monthly_contract_ind_tenant.xml',
        'views/Quarterly_cont_for_comp.xml',
        'views/Quarterly_cont_for_ind.xml',
        'views/yearly_contract_for_comp.xml',
        'views/yearly_contract_for_ind.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
