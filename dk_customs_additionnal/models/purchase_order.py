# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderDK(models.Model):
    _inherit = "purchase.order"

    @api.depends('state', )
    def _get_invoiced(self):
        for order in  self:
            super(PurchaseOrderDK, order)._get_invoiced()
            if order.amount_total == 0 and order.invoice_status == "to invoice" and order.invoice_ids != False:
                order.invoice_status = 'invoiced'
