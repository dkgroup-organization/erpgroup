# -*- coding: utf-8 -*-
from odoo import http

# class ProjetLiaisonsEtc(http.Controller):
#     @http.route('/projet_liaisons_etc/projet_liaisons_etc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/projet_liaisons_etc/projet_liaisons_etc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('projet_liaisons_etc.listing', {
#             'root': '/projet_liaisons_etc/projet_liaisons_etc',
#             'objects': http.request.env['projet_liaisons_etc.projet_liaisons_etc'].search([]),
#         })

#     @http.route('/projet_liaisons_etc/projet_liaisons_etc/objects/<model("projet_liaisons_etc.projet_liaisons_etc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('projet_liaisons_etc.object', {
#             'object': obj
#         })