# -*- coding: utf-8 -*-
# from odoo import http


# class DkProject(http.Controller):
#     @http.route('/dk_project/dk_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dk_project/dk_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dk_project.listing', {
#             'root': '/dk_project/dk_project',
#             'objects': http.request.env['dk_project.dk_project'].search([]),
#         })

#     @http.route('/dk_project/dk_project/objects/<model("dk_project.dk_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dk_project.object', {
#             'object': obj
#         })
