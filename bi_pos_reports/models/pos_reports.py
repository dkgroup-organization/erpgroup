# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, tools
from datetime import date, datetime


class POSConfigSummery(models.Model):
	_inherit = 'pos.config'

	order_summery = fields.Boolean('Order Summery')
	product_summery = fields.Boolean('Product Summery')
	product_categ_summery = fields.Boolean('Product product Summery')
	loc_summery = fields.Boolean('Audit Report')
	payment_summery = fields.Boolean('Payment Summery')


class PosOrderSummery(models.Model):
	_inherit = 'pos.order'

	def update_order_summery(self, ord_st_date, ord_end_date, ord_state, curr_session, order_current_session):
		to_day_date = datetime.now().date()
		summery_order = []
		if order_current_session:
			if ord_state == 'Select State':
				orders = self.env['pos.order'].search([
					('session_id', '=', curr_session),
					('state', 'in', ['paid', 'invoiced', 'done']),
				])
			else:
				orders = self.env['pos.order'].search([
					('session_id', '=', curr_session),
					('state', '=', ord_state.lower()),
				])

		else:
			if ord_state == 'Select State':
				orders = self.env['pos.order'].search([
					('date_order', '>=', ord_st_date + ' 00:00:00'),
					('date_order', '<=', ord_end_date + ' 23:59:59'),
					('state', 'in', ['paid', 'invoiced', 'done']),
				])
			else:
				orders = self.env['pos.order'].search([
					('date_order', '>=', ord_st_date + ' 00:00:00'),
					('date_order', '<=', ord_end_date + ' 23:59:59'),
					('state', '=', ord_state.lower()),
				])
		for order in orders:
			date = order.date_order.strftime('%Y-%m-%d')
			summery_order.append({'name': order.name, 'total': order.amount_total, 'date': date, 'state': order.state})

		return summery_order

	def update_product_summery(self, pro_st_date, pro_ed_date, prod_current_session, curr_session):
		config_obj = self.env['pos.config'].search([])

		# if prod_current_session:
		orders = self.env['pos.order'].search([
				('session_id', '=', curr_session),
				('state', 'in', ['paid', 'invoiced', 'done']),
				('config_id', 'in', config_obj.ids)])

		# else:
		# 	orders = self.env['pos.order'].search([
		# 		('date_order', '>=', pro_st_date + ' 00:00:00'),
		# 		('date_order', '<=', pro_ed_date + ' 23:59:59'),
		# 		('state', 'in', ['paid', 'invoiced', 'done']),
		# 		('config_id', 'in', config_obj.ids)])

		pos_line_ids = self.env["pos.order.line"].search([('order_id', 'in', orders.ids)]).ids

		if pos_line_ids:
			self.env.cr.execute("""
				SELECT product_tmpl.name, sum(pos_line.qty) total, product_tmpl.list_price prix, categ.name categ
				FROM pos_order_line AS pos_line,
					 pos_order AS pos_ord,
					 product_product AS product,
					 product_template AS product_tmpl,
					 pos_category AS categ
				WHERE pos_line.product_id = product.id
				    AND product_tmpl.pos_categ_id =categ.id
					AND product.product_tmpl_id = product_tmpl.id
					AND pos_line.order_id = pos_ord.id
					AND pos_line.id IN %s 
				GROUP BY product_tmpl.name, product_tmpl.list_price, categ.name
				ORDER BY categ.name
				
			""", (tuple(pos_line_ids),))
			products = self.env.cr.dictfetchall()
		else:
			products = []

		return products


class LocationSumm(models.Model):
	_name = "pos.order.location"

	@api.model
	def get_audit_by_session(self, select_session):
		prod_data = {}
		session_id = self.env['pos.session'].browse(int(select_session))
		orders = self.env['pos.order'].search([
			('session_id', '=', session_id.id),
			('state', 'in', ['paid', 'invoiced', 'done']),
		])
		for line in orders.mapped('lines'):
			quants = self.env['stock.quant'].search([('product_id.id', '=', line.product_id.id),
													 ('location_id.id', '=',
													  session_id.config_id.picking_type_id.default_location_src_id.id)])
			self.set_prod_data(line, prod_data, quants)
		return prod_data

	@api.model
	def get_audit_by_location(self, location):
		prod_data = {}
		orders = self.env['pos.order'].search([
			('state', 'in', ['paid', 'invoiced', 'done']),
		])
		location_id = int(location)
		for odr in orders:
			if odr.location_id.id == location_id:
				for line in odr.lines:
					quants = self.env['stock.quant'].search(
						[('product_id.id', '=', line.product_id.id), ('location_id.id', '=', location_id)])
					self.set_prod_data(line, prod_data, quants)
		return prod_data

	def set_prod_data(self, line, prod_data, quants):
		product = line.product_id.name
		if product in prod_data:
			old_qty = prod_data[product]['qty']
			prod_data[product].update({
				'qty': old_qty + line.qty,
			})
		else:
			if len(quants) > 1:
				quantity = 0.0
				for quant in quants:
					quantity += quant.quantity

				prod_data.update({product: {
					'product_id': line.product_id.id,
					'product_name': line.product_id.name,
					'qty': line.qty,
					'avail_qty': quantity,
				}})
			else:
				prod_data.update({product: {
					'product_id': line.product_id.id,
					'product_name': line.product_id.name,
					'qty': line.qty,
					'avail_qty': quants.quantity,
				}})
