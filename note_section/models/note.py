# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import xml.etree.ElementTree as xee
from odoo import api, models, fields, _
from datetime import datetime
from odoo.addons import decimal_precision as dp
class PurchaseLines(models.Model):
    _inherit = 'purchase.order.line'
    # pdf = fields.Boolean('afficher dans les document ?')
  
    order_id = fields.Many2one('purchase.order', string='Order Reference', index=True, required=False, ondelete='cascade')

    # @api.model
    # def create(self, values):
    #     if values.get('display_type', self.default_get(['display_type'])['display_type']):
    #         values.update(product_id=False, price_unit=0, product_uom_qty=0, product_uom=False, customer_lead=0)
    #     line = super(PurchaseLines, self).create(values)
    #     return line

    # def write(self, values):
    #     if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
    #         raise UserError("You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type.")
    #     result = super(PurchaseLines, self).write(values)
    #     return result

class stockopicking(models.Model):
    _inherit = 'stock.picking'
    # pdf = fields.Boolean('afficher dans les document ?')
  
    x_lines = fields.One2many('purchase.order.line','order_id',string="orders")



  