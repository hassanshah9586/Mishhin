{
    'name': "Integrating Maintenance Request with Inventory Module. ",
    'version': '14.0.1.0.0',
    'depends': ['base', 'stock', 'maintenance', 'property_maintenance_ee'],
    'license': 'LGPL-3',
    'data': [
        'views/maintenance_request.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}