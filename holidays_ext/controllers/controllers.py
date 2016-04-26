# -*- coding: utf-8 -*-
from openerp import http

# class HolidayExt(http.Controller):
#     @http.route('/holiday_ext/holiday_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/holiday_ext/holiday_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('holiday_ext.listing', {
#             'root': '/holiday_ext/holiday_ext',
#             'objects': http.request.env['holiday_ext.holiday_ext'].search([]),
#         })

#     @http.route('/holiday_ext/holiday_ext/objects/<model("holiday_ext.holiday_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('holiday_ext.object', {
#             'object': obj
#         })