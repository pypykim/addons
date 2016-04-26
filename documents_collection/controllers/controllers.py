# -*- coding: utf-8 -*-
from openerp import http

# class DocumentsExt(http.Controller):
#     @http.route('/documents_ext/documents_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/documents_ext/documents_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('documents_ext.listing', {
#             'root': '/documents_ext/documents_ext',
#             'objects': http.request.env['documents_ext.documents_ext'].search([]),
#         })

#     @http.route('/documents_ext/documents_ext/objects/<model("documents_ext.documents_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('documents_ext.object', {
#             'object': obj
#         })