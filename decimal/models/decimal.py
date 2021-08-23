# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from odoo.addons import decimal_precision as dp


class DecimalPpprecisionn(models.Model):
    _inherit = 'purchase.order.line'
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Test'), required=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Test'))
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', store=True,digits=dp.get_precision('Test'))
    price_total = fields.Float(compute='_compute_amount', string='Total', store=True,digits=dp.get_precision('Test'))