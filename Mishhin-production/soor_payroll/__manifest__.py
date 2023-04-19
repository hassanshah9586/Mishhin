# See LICENSE file for full copyright and licensing details
{
    'name': 'Kuwait Payroll',
    'version': '14.0.1.0.0',
    'category': 'Real Estate',
    'summary': """
        Kuwait Payroll
     """,
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.in/product/property-management-system',
    'depends': ['hr','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/payroll_configration_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_contract_view.xml',

    ],
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': True,
}
