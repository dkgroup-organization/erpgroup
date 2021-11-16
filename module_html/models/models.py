from odoo import api, fields, models


import logging
_logger = logging.getLogger(__name__)



class cate(models.Model):
    _inherit = "sale.order"
    name = fields.Text(string='Description', required=True)