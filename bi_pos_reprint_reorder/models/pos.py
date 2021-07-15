# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from datetime import date, datetime


class pos_order(models.Model):
	_inherit = 'pos.order'

	def print_pos_receipt(self):
		output = []
		discount = 0
		order_id = self.search([('id', '=', self.id)], limit=1)
		barcode = order_id.barcode
		orderlines = self.env['pos.order.line'].search([('order_id', '=', order_id.id)])
		payments = self.env['pos.payment'].search([('pos_order_id', '=', order_id.id)])
		paymentlines = []
		subtotal = 0
		tax = 0
		change = 0
		for payment in payments:
			if payment.amount > 0:
				temp = {
					'amount': payment.amount,
					'name': payment.payment_method_id.name
				}
				paymentlines.append(temp)
			else:
				change += payment.amount
			 
		for orderline in orderlines:
			new_vals = {
				'product_id': orderline.product_id.name,
				'total_price' : orderline.price_subtotal_incl,
				'qty': orderline.qty,
				'price_unit': orderline.price_unit,
				'discount': orderline.discount,
				}
				
			discount += (orderline.price_unit * orderline.qty * orderline.discount) / 100
			subtotal +=orderline.price_subtotal
			tax += (orderline.price_subtotal_incl - orderline.price_subtotal)
			
			output.append(new_vals)

		return [output, discount, paymentlines, change, subtotal, tax,barcode]

