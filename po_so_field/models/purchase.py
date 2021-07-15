# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one(
        'sale.order',
        "Sale Order",
        help="Reference to Sale Order",
    )
