# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _

class laivraison(models.Model):
    _inherit = 'stock.picking'

    user_id = fields.Many2one('res.users',
        ondelete='set null', string="Résponsable", index=True)
    x_contact = fields.Many2one('res.partner',
        ondelete='set null', string="Contact Fournisseur", index=True)
    x_objet = fields.Char("Objet")
    x_lines = fields.One2many(
        'purchase.order.line', 'order_id', string="orders")