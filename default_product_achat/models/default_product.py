# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _

class default_purchase(models.Model):
    _inherit = 'purchase.order.line'
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True, required=False, default= lambda self: self.env['product.product'].search([('name','=','Line')]))