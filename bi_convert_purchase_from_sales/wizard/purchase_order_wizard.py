# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning





class addfieldpurchase(models.Model):
    _inherit = 'sale.order'
    vents_lies = fields.Many2many("purchase.order",'sale_order_move_rel',string="Ventes liés")
    somme = fields.Float(string="Total achats", compute='_count_somme',readonly=True)
    marge = fields.Float(string="Marge bénéficiaire", compute='_count_marge', readonly=True)
    montant_impact = fields.Float(string="Montant impacter sur l'achat",digits=dp.get_precision('Product Price'),store=True )


    def delier(self):
     data = self.env['purchase.order'].search([('id','=',self.purchase_order_id.id)])

     for n in data:
     	data.montant_impact = data.montant_impact - self.montant_impact
     	self.vents_lies   = [(3, self.purchase_order_id.id)]
     	data.vents_lies2 =  [(3, self.id)]
    

    def _count_somme(self):
        for l in self:
          l.somme = 0
        # for line in self.vents_lies:
        #         self.somme = self.somme+ line.amount_untaxed
        # return self.somme

    def _count_marge(self):
        self.marge = self.amount_untaxed - self.somme
        return self.marge



class addfieldpurchase(models.Model):
    _inherit = 'purchase.order'
    vents_lies2 = fields.Many2many("sale.order",'purchase_move_rel',string="Ventes liés") 
    vents_lies3 = fields.Many2many("account.move",'account_move_rel',string="Facture liés")  
    somme = fields.Float(string="Total ventes", compute='_count_somme',readonly=True)
    marge = fields.Float(string="Marge bénéficiaire", compute='_count_marge', readonly=True)
    invoice_order_id = fields.Many2one(
        'account.move',
        "Facture client lié",
        help="Reference to invoice",
    )
    montant_impact = fields.Float(string="Montant impacter par des ventes",digits=dp.get_precision('Product Price'),store=True )

    restant = fields.Float(string="Montant réstant",digits=dp.get_precision('Product Price'),store=True, compute= '_compute' )

    def delier(self):
    	data = self.env['sale.order'].search([('id','=',self.sale_order_id.id)])
    	for m in data:
    		self.montant_impact = self.montant_impact - m.montant_impact
    		self.vents_lies2   = [(3, m.id)]
    		m.vents_lies = [(3, self.id)]

    def delier2(self):
    	data = self.env['account.move'].search([('id','=',self.move_order_id.id)])
    	for m in data:
    		self.montant_impact = self.montant_impact - m.montant_impact
    		self.vents_lies3   = [(3, m.id)]
    		m.achats = [(3, self.id)]


    @api.depends('amount_untaxed', 'montant_impact')
    def _compute(self):
    	for m in self:
    		m.restant = m.amount_untaxed - m.montant_impact

    def _count_somme(self):
        self.somme = 0
        for line in self.vents_lies2:
                self.somme = self.somme+ line.amount_untaxed
        for line2 in self.vents_lies3:
        		self.somme = self.somme+ line2.amount_untaxed
        return self.somme

    def _count_marge(self):
        self.marge = self.somme - self.amount_untaxed
        return self.marge





class addfieldpurchase(models.Model):
    _inherit = 'account.move'
    
    achats = fields.Many2many("purchase.order",'facturee_move_rel',string="Achats liés") 
    somme_achat = fields.Float(string="Total Facture achats", compute='_count_somme_achat',readonly=True)
    somme_vente = fields.Float(string="Total Facture ventes", compute='_count_somme_vente',readonly=True)
    marge_achat = fields.Float(string="Marge bénéficiaire", compute='_count_marge_achat', readonly=True)
    marge_vente = fields.Float(string="Marge bénéficiaire", compute='_count_marge_vente', readonly=True)
    purchase_order_id = fields.Many2one(
        'purchase.order',
        "Purchase Order",
        help="Reference to Purchase Order",
    )
    montant_impact = fields.Float(string="Montant impacter sur l'achat",digits=dp.get_precision('Product Price'),store=True )


    def delier(self):
     data = self.env['purchase.order'].search([('id','=',self.purchase_order_id.id)])
     for m in data:
       self.montant_impact = self.montant_impact - m.montant_impact
       self.achats   = [(3, m.id)]
       m.vents_lies3 = [(3, self.id)]
       

    def _count_somme_achat(self):
       for m in self:
           m.somme_achat = 0
           for line in m.achats:
               m.somme_achat = m.somme_achat + line.amount_untaxed



    def _count_somme_vente(self):
        for m in self:
         m.somme_vente = 0
     
     

    def _count_marge_achat(self):
        for m in self:
            m.marge_achat = m.amount_untaxed - m.somme_achat


    def _count_marge_vente(self):
        for m in self:
         m.marge_vente = 0



















class createpurchaseorder(models.TransientModel):
	_name = 'create.purchaseorder'
	_description = "Create Purchase Order"

	new_order_line_ids = fields.One2many( 'getsale.orderdata', 'new_order_line_id',String="Lignes de commande")
	partner_id = fields.Many2one('res.partner', string='Fournisseur', required = True)
	date_order = fields.Datetime(string='Date de la commande', required=True, copy=False, default=fields.Datetime.now)
	order_id = fields.Many2one('sale.order', string='Vente liés', required = False, compute= '_compute')
	tout_lignes = fields.Boolean('Aouter toutes les linges')
	montant_lie = fields.Float(string='Montant à lier', required=True, digits=dp.get_precision('Product Price'))
	

	
	def _compute(self):
		self.order_id = self.env['sale.order'].browse(self._context.get('active_ids',[])).id

	@api.model
	def default_get(self,  default_fields):
		res = super(createpurchaseorder, self).default_get(default_fields)
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		update = []
		seller_ids = []
		for record in data.order_line:
			update.append((0,0,{
							'product_id' : record.product_id.id,
							'product_uom' : record.product_uom.id,
							'order_id': record.order_id.id,
							'name' : record.name,
							'product_qty' : record.product_uom_qty,
							'price_unit' : record.price_unit,
							'product_subtotal' : record.price_subtotal,
							'display_type': record.display_type,
							'taxes_id':[(6, 0,record.tax_id.ids)],
							}))
		res.update({'new_order_line_ids':update})
		return res

	def action_create_purchase_order(self):
		self.ensure_one()
		res = self.env['purchase.order'].browse(self._context.get('id',[]))
		value = []
		pricelist = self.partner_id.property_product_pricelist
		partner_pricelist = self.partner_id.property_product_pricelist
		partner = self.partner_id
		counter = 0
		for count in self.new_order_line_ids:
			if count.product_id:
				counter = counter+1
		for data in self.new_order_line_ids:
		  if self.tout_lignes == True:
			  if self.montant_lie > 0 :
				  product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
				  final_price = self.montant_lie/counter
			
			  else:
				  final_price = data.product_id.standard_price
			 	
			  value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'date_planned' : datetime.now(),
								'price_unit' : final_price,
								'display_type': data.display_type,
								'taxes_id' : [(6, 0, data.taxes_id.ids)],
								}])



		  else:

			  for m in data.product_id.seller_ids:
			   if partner == m.name:
			    four = m  	
			    value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'date_planned' : datetime.now(),
								'price_unit' : four.price,
								'display_type': data.display_type,
								'taxes_id' : [(6, 0, data.taxes_id.ids)],
								}])
		res.create({
						'sale_order_id' : self.order_id.id,
						'vents_lies2'   : [(4, self.order_id.id)],
						'partner_id' : self.partner_id.id,
						'date_order' : str(self.date_order),
						'order_line':value,
						
					})

		
		search_ids = self.env['purchase.order'].search([('date_order','=',self.date_order)])
		last_id = search_ids and max(search_ids)      
		return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'purchase.order',
        'target': 'current',
        'res_id': search_ids.id,
        'context': {'form_view_initial_mode': 'edit','force_detailed_view': True},
         }



class Getsaleorderdata(models.TransientModel):
	_name = 'getsale.orderdata'
	_description = "Get Sale Order Data"

	new_order_line_id = fields.Many2one('create.purchaseorder')
		
	product_id = fields.Many2one('product.product', string="Article", required=False)
	name = fields.Char(string="Description")
	product_qty = fields.Float(string='Quantité', required=False)
	date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
	product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
	order_id = fields.Many2one('sale.order', string='Order Reference', required=False, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	display_type = fields.Selection([
      ('line_section', "Section"),
      ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
	taxes_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit

class Ajouter_achat(models.TransientModel):
	_name = 'ajouter.achat'
	_description = "Ajouter Achat"

	
	achat = fields.Many2one('purchase.order', string='Achats', required = True)
	fournisseur = fields.Char('Fournisseur',readonly=True)
	total = fields.Char('Total',readonly=True)
	date = fields.Char('Date',readonly=True)
	responsable = fields.Char('Responsable Achats',readonly=True)
	montant_impact = fields.Float(string="Montant à impacter",readonly=False,store=True)

	@api.onchange('achat')
	def _onchange_achat(self):
			self.fournisseur = self.achat.partner_id.name
			self.total = self.achat.amount_untaxed
			self.date = self.achat.date_order
			self.responsable = self.achat.user_id.name
			self.montant_impact = self.achat.amount_untaxed - self.achat.montant_impact

	# @api.depends('achat')
	# def _compute_total(self):
	# 	self.montant_impact = self.achat.amount_total - self.achat.montant_impact
	

	def action_add_achat(self):
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		
		data.montant_impact = self.montant_impact
		data.vents_lies = [(4, self.achat.id)]
		self.achat.vents_lies2   = [(4, data.id)]
		self.achat.sale_order_id = data.id
		data.purchase_order_id = self.achat.id
		if self.achat.montant_impact <= self.achat.amount_untaxed and self.achat.montant_impact + self.montant_impact <= self.achat.amount_untaxed :
		  self.achat.montant_impact = self.achat.montant_impact + self.montant_impact
		else:
			raise Warning(_("vous avez dépassé le montant total de l\'achat"))

class Ajouter_achat_fact(models.TransientModel):
	_name = 'ajouter.achat_fact'
	_description = "Ajouter Achat facture"

	
	achat = fields.Many2one('purchase.order', string='Achats', required = True)
	fournisseur = fields.Char('Fournisseur',readonly=True)
	total = fields.Char('Total',readonly=True)
	date = fields.Char('Date',readonly=True)
	responsable = fields.Char('Responsable Achats',readonly=True)
	montant_impact = fields.Float(string="Montant à impacter",readonly=False,store=True)


	@api.onchange('achat')
	def _onchange_achat(self):
			self.fournisseur = self.achat.partner_id.name
			self.total = self.achat.amount_total
			self.date = self.achat.date_order
			self.responsable = self.achat.user_id.name
			self.montant_impact = self.achat.amount_untaxed - self.achat.montant_impact

	

	def action_add_achat(self):
		data = self.env['account.move'].browse(self._context.get('active_ids',[]))
		data.montant_impact = self.montant_impact
		self.achat.invoice_order_id = data.id
		data.purchase_order_id = self.achat.id
		self.achat.vents_lies3   = [(4, data.id)]
		data.achats = [(4, self.achat.id)]
		if self.achat.montant_impact <= self.achat.amount_untaxed and self.achat.montant_impact + self.montant_impact <= self.achat.amount_untaxed :
		  self.achat.montant_impact = self.achat.montant_impact + self.montant_impact
		else:
			raise Warning(_("vous avez dépassé le montant total de l\'achat"))




class Ajouter_vente(models.TransientModel):
		_name = 'ajouter.vente'
		_description = "Ajouter Vente"

		typo = fields.Selection(string='Type de document',selection=[('dev', 'Devis'), ('fact', 'Facture')])

		vente = fields.Many2one('sale.order', string='Devis', required = False)
		vente2 = fields.Many2one('account.move', string='Facture', required = False)
		client = fields.Char('Client',readonly=True)
		total = fields.Char('Total',readonly=True)
		date = fields.Char('Date de la commande',readonly=True)
		vendeur = fields.Char('Vendeur',readonly=True)
		montant_impact = fields.Float(string="Montant de l'achat à impacter",readonly=False,store=True)
		

		@api.onchange('vente')
		def _onchange_vente(self):
				data = self.env['purchase.order'].browse(self._context.get('active_ids',[]))
				self.client = self.vente.partner_id.name
				self.total = self.vente.amount_total
				self.date = self.vente.date_order
				self.vendeur = self.vente.user_id.name
				self.montant_impact = data.amount_untaxed - data.montant_impact



		@api.onchange('vente2')
		def _onchange_vente22(self):
				data = self.env['purchase.order'].browse(self._context.get('active_ids',[]))
				self.client = self.vente2.partner_id.name
				self.total = self.vente2.amount_total
				self.date = self.vente2.date_invoice
				self.vendeur = self.vente2.user_id.name
				self.montant_impact = data.amount_untaxed - data.montant_impact
			

		def action_add_vente(self):
			data = self.env['purchase.order'].browse(self._context.get('active_ids',[]))
			if self.vente:
						
		 		self.vente.purchase_order_id = data.id
		 		self.vente.vents_lies   = [(4, data.id)]
		 		data.vents_lies2 = [(4, self.vente.id)]
		 		if data.montant_impact <= data.amount_untaxed and data.montant_impact + self.montant_impact <= data.amount_untaxed:
		 			data.montant_impact = data.montant_impact + self.montant_impact
		 			self.vente.montant_impact = self.montant_impact
		 		else:
		 			raise Warning(_("vous avez dépassé le montant total de l\'achat"))


			if self.vente2:
				self.vente2.purchase_order_id = data.id
				self.vente2.achats   = [(4, data.id)]
				data.vents_lies3 = [(4, self.vente2.id)]
				if data.montant_impact <= data.amount_untaxed and data.montant_impact + self.montant_impact <= data.amount_untaxed:
					data.montant_impact = data.montant_impact + self.montant_impact
					self.vente2.montant_impact = self.montant_impact
				else:
					raise Warning(_("vous avez dépassé le montant total de l\'achat"))














class createsaleorder(models.TransientModel):
	_name = 'create.saleorder'
	_description = "Create Sale Order"

	new_order_line_ids = fields.One2many( 'getpurchase.orderdata', 'new_order_line_id',String="Lignes de commande")
	partner_id = fields.Many2one('res.partner', string='Client', required = True)
	date_order = fields.Datetime(string='Date de la commande', required=True, copy=False, default=fields.Datetime.now)
	order_id = fields.Many2one('purchase.order', string='achat liés', required = False, compute= '_compute')
	tout_lignes = fields.Boolean('Aouter toutes les linges')
	par_montant = fields.Boolean('Créer devis par montant')
	montant_devis = fields.Float(string='Montant de la commande', required=True, digits=dp.get_precision('Product Price'))

	
	def _compute(self):
		self.order_id = self.env['purchase.order'].browse(self._context.get('active_ids',[])).id

	@api.model
	def default_get(self,  default_fields):
		res = super(createsaleorder, self).default_get(default_fields)
		data = self.env['purchase.order'].browse(self._context.get('active_ids',[]))
		update = []
		seller_ids = []
		prod_id = self.env['product.product'].search([('name','=','Ligne')])

		for record in data.order_line:
			if record.product_id:
				update.append((0,0,{
							'product_id' : record.product_id.id,
							'product_uom' : record.product_uom.id,
							'order_id': record.order_id.id,
							'name' : record.name,
							'product_qty' : record.product_uom_qty,
							'price_unit' : record.price_unit,
							'product_subtotal' : record.price_subtotal,
							'display_type': record.display_type,
							}))
			else:
				update.append((0,0,{
							'product_id' : prod_id.id,
							'product_uom' : record.product_uom.id,
							'order_id': record.order_id.id,
							'name' : record.name,
							'product_qty' : 1,
							'price_unit' : record.price_unit,
							'product_subtotal' : record.price_subtotal,
							'display_type': record.display_type,
							}))



		res.update({'new_order_line_ids':update})
		return res

	def action_create_sale_order(self):
		self.ensure_one()
		res = self.env['sale.order'].browse(self._context.get('id',[]))
		value = []
		pricelist = self.partner_id.property_product_pricelist
		partner_pricelist = self.partner_id.property_product_pricelist
		partner = self.partner_id
		counter = 0
		for count in self.new_order_line_ids:
			if count.display_type == False:
				counter = counter+1
		for data in self.new_order_line_ids:
			if 	self.par_montant == False:
			  if partner_pricelist:
				  product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
				  final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id, data.product_qty or 1.0, self.partner_id)
			
			  else:
				  final_price = data.product_id.lst_price
			 	
			  value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_uom_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'price_unit' : data.product_id.list_price,
								'display_type': data.display_type,
								}])

			else:
			  value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_uom_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'price_unit' : self.montant_devis/(counter*data.product_qty),
								'display_type': data.display_type,
								}])



		res.create({
						'purchase_order_id' : self.order_id.id,
						'vents_lies'   : [(4, self.order_id.id)],
						'partner_id' : self.partner_id.id,
						'date_order' : str(self.date_order),
						'order_line':value,
						
					})

		
		search_ids = self.env['sale.order'].search([('date_order','=',self.date_order)])
		last_id = search_ids and max(search_ids)      
		return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'sale.order',
        'target': 'current',
        'res_id': search_ids.id,
        'context': {'form_view_initial_mode': 'edit','force_detailed_view': True},
         }



class Getpurchaseorderdata(models.TransientModel):
	_name = 'getpurchase.orderdata'
	_description = "Get Sale Order Data"

	new_order_line_id = fields.Many2one('create.saleorder')
		
	product_id = fields.Many2one('product.product', string="Article", required=True)
	name = fields.Char(string="Description")
	product_qty = fields.Float(string='Quantité', required=True)
	date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
	product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
	order_id = fields.Many2one('purchase.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	display_type = fields.Selection([
      ('line_section', "Section"),
      ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit



































class createpurchaseorderfact(models.TransientModel):
	_name = 'create.purchaseorderfact'
	_description = "Create Purchase Order"

	new_order_line_ids = fields.One2many( 'getinvoice.orderdata', 'new_order_line_id',String="Lignes de commande")
	partner_id = fields.Many2one('res.partner', string='Fournisseur', required = True)
	date_order = fields.Datetime(string='Date de la commande', required=True, copy=False, default=fields.Datetime.now)
	invoice_id = fields.Many2one('account.move', string='Facture liés', required = False, compute= '_compute')
	tout_lignes = fields.Boolean('Aouter toutes les linges')
	montant_lie = fields.Float(string='Montant à lier', required=True, digits=dp.get_precision('Product Price'))

	
	def _compute(self):
		self.invoice_id = self.env['account.move'].browse(self._context.get('active_ids',[])).id

	@api.model
	def default_get(self,  default_fields):
		res = super(createpurchaseorderfact, self).default_get(default_fields)
		data = self.env['account.move'].browse(self._context.get('active_ids',[]))
		update = []
		seller_ids = []
		for record in data.invoice_line_ids:
			update.append((0,0,{
							'product_id' : record.product_id.id,
							'product_uom' : record.product_uom_id.id,
							# 'invoice_id': record.move_id.id,
							'name' : record.name,
							'product_qty' : record.quantity,
							'price_unit' : record.price_unit,
							'product_subtotal' : record.price_subtotal,
							'display_type': record.display_type,

							}))
		res.update({'new_order_line_ids':update})
		return res

	def action_create_purchase_orderfact(self):
		self.ensure_one()
		res = self.env['purchase.order'].browse(self._context.get('id',[]))
		value = []
		pricelist = self.partner_id.property_product_pricelist
		partner_pricelist = self.partner_id.property_product_pricelist
		partner = self.partner_id
		for data in self.new_order_line_ids:
		  if self.tout_lignes == True:
			  if self.montant_lie > 0 :
				  product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
				  final_price = self.montant_lie/len(self.new_order_line_ids)
			
			  else:
				  final_price = data.price_unit
			 	
			  value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								# 'invoice_lines':data.invoice_id.id,
								# 'order_id':res.id,
								'product_uom' : 1,
								'date_planned' : self.date_order,
								'price_unit' : final_price,
								'display_type': data.display_type,
								}])



		  else:
			  
			  for m in data.product_id.seller_ids:
			   if partner == m.name:
			    four = m  	  	
			    value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								# 'invoice_lines':data.invoice_id.id,
								# 'order_id':res.id,
								'product_uom' : 1,
								'date_planned' : self.date_order,
								'price_unit' : four.price,
								'display_type': data.display_type,
								}])
		res.create({
						'invoice_order_id' : self.invoice_id.id,
						'vents_lies3'   : [(4, self.invoice_id.id)],
						'partner_id' : self.partner_id.id,
						'date_order' : str(self.date_order),
						'order_line':value,

						
					})

		
		search_ids = self.env['purchase.order'].search([])
		last_id = search_ids and max(search_ids)      
		return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'purchase.order',
        'target': 'current',
        'res_id': last_id.id,
        'context': {'form_view_initial_mode': 'edit','force_detailed_view': True},
         }



class Getinvoicedata(models.TransientModel):
	_name = 'getinvoice.orderdata'
	_description = "Get Invoice Order Data"

	new_order_line_id = fields.Many2one('create.purchaseorderfact')
		
	product_id = fields.Many2one('product.product', string="Article", required=False)
	name = fields.Char(string="Description")
	product_qty = fields.Float(string='Quantité', required=False)
	date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
	product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
	invoice_id = fields.Many2one('account.move', string='invoice Reference', required=False, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=False, digits=dp.get_precision('Product Price'))
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	display_type = fields.Selection([
      ('line_section', "Section"),
      ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit

















class delier_achat(models.TransientModel):
	_name = 'delier.achat'
	_description = "delier Achat"

	
	achat = fields.Many2one('purchase.order', string='Achats', required = True)
	
	

	
	@api.onchange('achat')
	def _getfilter(self):
		data = self.env['sale.order'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'achat': [('id', 'in', data.vents_lies.ids)]}}
	def action_delier_achat(self):
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		for m in data:
			self.achat.montant_impact = self.achat.montant_impact - m.montant_impact
			self.achat.vents_lies2   = [(3, m.id)]
			m.vents_lies = [(3, self.achat.id)]


	






class delier_vente(models.TransientModel):
	_name = 'delier.vente'
	_description = "delier Vente"

	
	vente = fields.Many2one('sale.order', string='Ventes', required = True)
	
	

	
	@api.onchange('vente')
	def _getfilter(self):
		data = self.env['purchase.order'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'vente': [('id', 'in', data.vents_lies2.ids)]}}
	def action_delier_vente(self):
		data = self.env['purchase.order'].browse(self._context.get('active_ids',[]))
		for n in data:
			n.montant_impact = n.montant_impact - self.vente.montant_impact
			self.vente.vents_lies   = [(3, n.id)]
			n.vents_lies2 =  [(3, self.vente.id)]










class delier_facture(models.TransientModel):
	_name = 'delier.facture'
	_description = "delier facture"

	
	facture = fields.Many2one('account.move', string='Facture', required = True)
	
	

	
	@api.onchange('facture')
	def _getfilter(self):
		data = self.env['purchase.order'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'facture': [('id', 'in', data.vents_lies3.ids)]}}
	def action_delier_facture(self):
		data = self.env['purchase.order'].browse(self._context.get('active_ids',[]))

		for m in data:
				m.montant_impact = m.montant_impact - self.facture.montant_impact
				m.vents_lies3   = [(3, self.facture.id)]
				self.facture.achats = [(3, m.id)]









class delier_achat_fact(models.TransientModel):
	_name = 'delier.achat_fact'
	_description = "delier Achat fature"

	
	achat = fields.Many2one('purchase.order', string='Achats', required = True)
	
	

	
	@api.onchange('achat')
	def _getfilter(self):
		data = self.env['account.move'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'achat': [('id', 'in', data.achats.ids)]}}
	def action_delier_achat_fact(self):
		data = self.env['account.move'].browse(self._context.get('active_ids',[]))
		for m in data:
			self.achat.montant_impact = self.achat.montant_impact - m.montant_impact
			self.achat.vents_lies3   = [(3, m.id)]
			m.achats = [(3, self.achat.id)]



