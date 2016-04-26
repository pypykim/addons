# -*- coding: utf-8 -*-
from openerp import http

# class ProcurementRequest(http.Controller):
#     @http.route('/procurement_request/procurement_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/procurement_request/procurement_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('procurement_request.listing', {
#             'root': '/procurement_request/procurement_request',
#             'objects': http.request.env['procurement_request.procurement_request'].search([]),
#         })

#     @http.route('/procurement_request/procurement_request/objects/<model("procurement_request.procurement_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('procurement_request.object', {
#             'object': obj
#         })