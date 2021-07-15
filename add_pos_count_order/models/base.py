

from odoo import api, fields, models, _


class possessionordercount(models.Model):
    _inherit = 'pos.session'

    total_orders_amount = fields.Float(compute='_compute_total_orders_amount', string='Total order Amount')
    @api.depends('order_ids')
    def _compute_total_orders_amount(self):
        for session in self:
            session.total_orders_amount = sum(session.order_ids.mapped('amount_total'))