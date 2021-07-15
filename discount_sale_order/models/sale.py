# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.model
	def _wk_discount_settings(self):
		configModel = self.env['res.config.settings']
		vals = {
			'group_discount_per_so_line' : 1,
			'group_order_global_discount' : True,
			'global_discount_tax' : 'untax',
		}
		defaultSetObj = configModel.create(vals)
		defaultSetObj.execute()
		return True

	@api.depends('order_line.price_total', 'global_order_discount', 'global_discount_type')
	def _amount_all(self):
		for order in self:
			amount_untaxed = amount_tax = 0.0
			total_discount = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				if line.discount_type == 'fixed':
					total_discount += line.discount
				else:
					total_discount += line.product_uom_qty*(line.price_unit - line.price_reduce)
				if order.company_id.tax_calculation_rounding_method == 'round_globally':
					quantity = 1.0
					if line.discount_type == 'fixed':
						price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
					else:
						quantity = line.product_uom_qty
						price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
					taxes = line.tax_id.compute_all(price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
					amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
				else:
					amount_tax += line.price_tax

			IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
			discTax = IrConfigPrmtrSudo.get_param('sale.global_discount_tax')
			if discTax == 'untax':
				total_amount = amount_untaxed
			else:
				total_amount = amount_untaxed + amount_tax
			if order.global_discount_type == 'percent':
				beforeGlobal = total_amount
				total_amount = total_amount * (1 - (order.global_order_discount or 0.0)/100)
				total_discount += beforeGlobal - total_amount
			else:
				total_amount = total_amount - (order.global_order_discount or 0.0)
				total_discount += order.global_order_discount
			if discTax == 'untax':
				total_amount = total_amount + amount_tax
			order.update({
				'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
				'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
				'amount_total': total_amount,
				'total_discount': total_discount,
			})

	total_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
	global_discount_type = fields.Selection([
		('fixed', 'Fixed'),
		('percent', 'Percent')
		], string="Discount Type",)
	global_order_discount = fields.Float(string='Global Discount', store=True,  track_visibility='always')


	def _prepare_invoice(self):
		invoiceVals = super(SaleOrder, self)._prepare_invoice()
		self.ensure_one()
		if self.global_order_discount:
			invoiceVals.update({
				'global_discount_type' : self.global_discount_type,
				'global_order_discount' : self.global_order_discount
				})
		return invoiceVals

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	discount = fields.Float(string='Discount', digits=dp.get_precision('Discount'), default=0.0)
	line_amount_subtotal = fields.Monetary(compute='_get_price_reduce', string='Subtotal', readonly=True, store=True)
	line_amount_total = fields.Monetary(compute='_get_price_reduce', string='Total', readonly=True, store=True)
	discount_type = fields.Selection([
		('fixed', 'Fixed'),
		('percent', 'Percent')
		], string="Discount Type", default='percent')



	@api.depends('product_uom_qty','discount_type', 'discount', 'price_unit', 'tax_id')
	def _compute_amount(self):
		for line in self:
			quantity = 1.0
			if line.discount_type == 'fixed':
				price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
			else:
				price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
				quantity = line.product_uom_qty
			taxes = line.tax_id.compute_all(
				price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
			line.update({
				'price_tax': taxes['total_included'] - taxes['total_excluded'],
				'price_total': taxes['total_included'],
				'price_subtotal': taxes['total_excluded'],
			})

	@api.depends('price_unit', 'discount_type', 'discount', 'product_uom_qty', 'tax_id')
	def _get_price_reduce(self):
		for line in self:
			if line.discount_type == 'fixed' and line.product_uom_qty:
				price_reduce = line.price_unit * line.product_uom_qty - line.discount
				line.price_reduce = price_reduce/line.product_uom_qty
			else:
				line.price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
			price = line.price_unit
			quantity = line.product_uom_qty
			taxes = line.tax_id.compute_all(
				price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
			line.line_amount_subtotal = taxes['total_excluded']
			line.line_amount_total = taxes['total_included']

	def _prepare_invoice_line(self, qty):
		res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
		res.update(
			discount_type=self.discount_type,
			discount=self.discount
			)
		return res
