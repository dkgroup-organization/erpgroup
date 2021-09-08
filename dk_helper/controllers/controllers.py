# -*- coding: utf-8 -*-
from odoo import http

# class DkHelper(http.Controller):
#     @http.route('/dk_helper/dk_helper/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dk_helper/dk_helper/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dk_helper.listing', {
#             'root': '/dk_helper/dk_helper',
#             'objects': http.request.env['dk_helper.dk_helper'].search([]),
#         })

#     @http.route('/dk_helper/dk_helper/objects/<model("dk_helper.dk_helper"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dk_helper.object', {
#             'object': obj
#         })