# -*- coding: utf-8 -*-
# from odoo import http


# class TenancyReport(http.Controller):
#     @http.route('/tenancy_report/tenancy_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tenancy_report/tenancy_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tenancy_report.listing', {
#             'root': '/tenancy_report/tenancy_report',
#             'objects': http.request.env['tenancy_report.tenancy_report'].search([]),
#         })

#     @http.route('/tenancy_report/tenancy_report/objects/<model("tenancy_report.tenancy_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tenancy_report.object', {
#             'object': obj
#         })
