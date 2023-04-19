# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    "name": "KNET Payment Acquirer",
    "summary": """Integrating KNET Payment Gateway service with Odoo. The module allows the customers to make payments for their ecommerce orders using KNET Payment Gateway service.""",
    "description": """KNET Payment Gateway Payment Acquirer""",
    "version": "14.0.1.0",
    "author": "Kanak Infosystems LLP.",
    "website": "https://www.kanakinfosystems.com",
    "category": "Accounting/Payment",
    'license': 'OPL-1',
    "depends": ["payment"],
    "external_dependencies": {
        "python": ["pycryptodomex"]
    },
    "data": [
        "views/payment_acquirer_views.xml",
        "views/payment_acquirer_templates.xml",
        "data/payment_acquirer_data.xml",
    ],
    "images": ['static/description/banner.jpg'],
    "application": True,
    "installable": True,
    "price": 79.0,
    "currency": "EUR",
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
