# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company(models.Model):
#     _name = 'c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company.c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company'
#     _description = 'c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company.c:\bitnami\odoo-14.0.20210530-0\apps\odoo\data\addons\14.0\feet_state_company'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
