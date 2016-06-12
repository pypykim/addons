# -*- coding: utf-8 -*-
from openerp import http

# class CalendarEventCico(http.Controller):
#     @http.route('/calendar_event_cico/calendar_event_cico/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calendar_event_cico/calendar_event_cico/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('calendar_event_cico.listing', {
#             'root': '/calendar_event_cico/calendar_event_cico',
#             'objects': http.request.env['calendar_event_cico.calendar_event_cico'].search([]),
#         })

#     @http.route('/calendar_event_cico/calendar_event_cico/objects/<model("calendar_event_cico.calendar_event_cico"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calendar_event_cico.object', {
#             'object': obj
#         })