# -*- coding: utf-8 -*-
# from odoo import http


# class C:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feetStateCompany(http.Controller):
#     @http.route('/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company.listing', {
#             'root': '/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company',
#             'objects': http.request.env['c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company.c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company'].search([]),
#         })

#     @http.route('/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company/objects/<model("c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company.c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company.object', {
#             'object': obj
#         })
