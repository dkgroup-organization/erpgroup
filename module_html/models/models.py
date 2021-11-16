from odoo import api, fields, models


import logging
_logger = logging.getLogger(__name__)



class cate(models.Model):
    _inherit = "sale.order"
    name = fields.Html(string='Descriptio', required=True,store=True)
