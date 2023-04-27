# See LICENSE file for full copyright and licensing details
{
    'name': 'Property Management Soor Dev',
    'version': '14.0.1.1.5',
    'category': 'Real Estate',
    'summary':
    """
        This module provides dev as per soor requrements
    """,
    'license': 'LGPL-3',
    'author': 'Soor',
    'website': 'http://serpentcs.in/product/property-management-system',
    'depends': ['property_management_ee'],
    'demo': [],
    'data': [
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "data/data.xml",
        "views/property_configuration_view.xml",
        "views/view_case_information.xml",
        "views/view_account_analytic.xml",
        "views/view_tenant_partner.xml",
        "views/report_tenancy_rent_receipt_voucher_template.xml",
        "views/report_configuration_view.xml",
        "views/report_tenancy_contract.xml",
        "views/report_tenancy_warehouse_contract.xml",
        "views/report_tenant_payment_details.xml",
        "views/view_account_payment.xml",
        "views/view_crm_lead.xml",
        "views/report_tenant_payment_property.xml",
        "views/view_res_company.xml",
        "report/tenant_payment_details_report_views.xml",
        "data/data.xml",
        'wizard/view_tenancy_tenant_report.xml',
        'wizard/view_tenant_payment_property_details_report.xml'
    ],
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': True,
}
