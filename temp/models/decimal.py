# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
import logging
from odoo import api, fields, models, _
from odoo.tools.misc import format_date
from odoo.osv import expression
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

class DecimalPprecision(models.Model):
    _inherit = 'sale.order'

    vents_lies = fields.Many2many("purchase.order",'sale_order_move_rel',string="Ventes liés")
    somme = fields.Float(string="Total achats", compute='_count_somme',readonly=True)
    marge = fields.Float(string="Marge bénéficiaire", compute='_count_marge', readonly=True)
    recompute_delivery_price = fields.Boolean('Delivery cost should be recomputed')
   



