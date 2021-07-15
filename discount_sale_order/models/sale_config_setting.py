# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_order_global_discount = fields.Boolean("A global discount on sales order",
        implied_group='discount_sale_order.group_order_global_discount',
        help="""Allows to give a global discount on sales order. """)
    global_discount_tax = fields.Selection([
        ('untax', 'Untaxed amount'),
        ('taxed', 'Tax added amount'),
        ], "Global Discount Calculation",
        help="Global disount calculation will be ( \
                'untax' : Global discount will be applied before applying tax, \
                'taxed : Global disount will be applied after applying tax)")
    discount_account_so = fields.Many2one(
        'account.account',
        string="Discount Account",
        help="""Account for Global discount on sales order.""")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        IrConfigPrmtr.set_param(
            "sale.global_discount_tax", self.global_discount_tax
        )
        IrConfigPrmtr.set_param(
            "sale.discount_account_so", self.discount_account_so.id
        )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        globalDiscountTax = IrConfigPrmtr.get_param('sale.global_discount_tax')
        discount_account_so = int(IrConfigPrmtr.get_param('sale.discount_account_so'))
        res.update({
            'global_discount_tax' : globalDiscountTax,
            'discount_account_so' : discount_account_so,
        })

        return res
