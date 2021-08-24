# -*- coding: utf-8 -*-
from odoo import http

# class DkgroupCustumizations(http.Controller):
#     @http.route('/dkgroup_custumizations/dkgroup_custumizations/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dkgroup_custumizations/dkgroup_custumizations/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dkgroup_custumizations.listing', {
#             'root': '/dkgroup_custumizations/dkgroup_custumizations',
#             'objects': http.request.env['dkgroup_custumizations.dkgroup_custumizations'].search([]),
#         })

#     @http.route('/dkgroup_custumizations/dkgroup_custumizations/objects/<model("dkgroup_custumizations.dkgroup_custumizations"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dkgroup_custumizations.object', {
#             'object': obj
#         })