from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    cancel_delivery_order_for_po = fields.Boolean(string="Cancel Delivery Order?")
    cancel_invoice_for_po = fields.Boolean(string='Cancel Invoice?')
    cancel_done_picking = fields.Boolean(string='Cancel Done Delivery?')
    cancel_paid_invoice = fields.Boolean(string='Cancel Paid Invoice?')
