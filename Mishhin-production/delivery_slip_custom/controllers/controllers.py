# -*- coding: utf-8 -*-
# from odoo import http


# class DeliverySlipCustom(http.Controller):
#     @http.route('/delivery_slip_custom/delivery_slip_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_slip_custom/delivery_slip_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_slip_custom.listing', {
#             'root': '/delivery_slip_custom/delivery_slip_custom',
#             'objects': http.request.env['delivery_slip_custom.delivery_slip_custom'].search([]),
#         })

#     @http.route('/delivery_slip_custom/delivery_slip_custom/objects/<model("delivery_slip_custom.delivery_slip_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_slip_custom.object', {
#             'object': obj
#         })
