# -*- encoding: utf-8 -*-

{
    'name': 'Kuwait Chart of Accounts',
    'version': '14.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'category': 'Localization',
    'description': """
     Arabic localization for most arabic countries.
    """,
    'depends': ['account'],
    'data': [
        'data/account_account_type.xml',
        'data/l10n_kw_chart_data.xml',
        'data/account.account.template.csv',
        'data/account_chart_template_configure_data.xml',
    ],
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
    'application': True,
}
