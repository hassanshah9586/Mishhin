{
    'name': "Removing Rent Type in Configuration setting, Add more fields, Change the tenant type ",
    'version': '14.0.1.0.0',
    'depends': ['base', 'property_management_ee'],
    'license': 'LGPL-3',
    'data': [
        'views/rent_type_menu.xml',
        'views/account_analytic_account.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}