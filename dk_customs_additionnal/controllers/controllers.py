# -*- coding: utf-8 -*-
# from odoo import http


# class DkCustomsAdditionnal(http.Controller):
#     @http.route('/dk_customs_additionnal/dk_customs_additionnal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dk_customs_additionnal/dk_customs_additionnal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dk_customs_additionnal.listing', {
#             'root': '/dk_customs_additionnal/dk_customs_additionnal',
#             'objects': http.request.env['dk_customs_additionnal.dk_customs_additionnal'].search([]),
#         })

#     @http.route('/dk_customs_additionnal/dk_customs_additionnal/objects/<model("dk_customs_additionnal.dk_customs_additionnal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dk_customs_additionnal.object', {
#             'object': obj
#         })
