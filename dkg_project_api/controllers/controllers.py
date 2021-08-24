# -*- coding: utf-8 -*-
# from odoo import http


# class DkgProjectApi(http.Controller):
#     @http.route('/dkg_project_api/dkg_project_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dkg_project_api/dkg_project_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dkg_project_api.listing', {
#             'root': '/dkg_project_api/dkg_project_api',
#             'objects': http.request.env['dkg_project_api.dkg_project_api'].search([]),
#         })

#     @http.route('/dkg_project_api/dkg_project_api/objects/<model("dkg_project_api.dkg_project_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dkg_project_api.object', {
#             'object': obj
#         })
