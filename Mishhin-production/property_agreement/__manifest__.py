{
    'name': 'Agreement type',
    'description': 'Account Asset',
    'author': 'Ali Hassan',
    'data': [
        'views/account_asset_views.xml',
        'views/account_move_view.xml',
    ],
    'depends': ['property_ee', 'sale'],
    'installable': True,
    'auto-install': False,
    'sequence': 8,
    'application': True
}
