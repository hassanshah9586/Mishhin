# -*- coding: utf-8 -*-
{
    'name': "property_mgmt",

    'summary': """
        This is Property Management Module""",

    'description': """
        This is Property Management Module for ErpVision
    """,

    'author': "erpvision",
    'website': "http://www.erpvision.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'account_accountant'],

    # always loaded
    'data': [
        'views/product_template.xml',
    ],

    # only loaded in demonstration mode
    'auto_install': False,
    'installable': True,
    'application': True,
}



