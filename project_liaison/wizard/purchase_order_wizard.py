# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning





class projecto(models.Model):
    _inherit = 'project.project'
    devis = fields.Many2many("sale.order",'sale_order_move_rel1',string="Devis")
    achats = fields.Many2many("purchase.order",'sale_order_move_rel2',string="Achats")
    factures = fields.Many2many("account.move",'sale_order_move_rel3',string="Factures")
    date_debut = fields.Datetime(string='Date de Demmarage Chantier', required=False, copy=False, default=fields.Datetime.now)
    date_fin = fields.Datetime(string='Date de fin de chanier', required=False, copy=False, default=fields.Datetime.now)
    reference_chantier = fields.Char(string="Reference chantier")

    state = fields.Selection([
            ('draft', 'Projet Valide'),
            ('prod', 'Production'),
            ('fact', 'Facturation'),
            ('done', 'Terminé'),
            ('cancel', 'Annuler'),
            ],default='draft')
    
    def prod(self):
        self.write({
        'state': 'prod',
    })
    def fact(self):
        self.write({
        'state': 'fact',
    })
    def done(self):
        self.write({
        'state': 'done',
    })
    def cancel(self):
        self.write({
        'state': 'cancel',
    })
    def draft(self):
        self.write({
        'state': 'draft',
    })




    
class projectt(models.Model):
    _inherit = 'sale.order'

    projet =  fields.Many2one('project.project',"Projet",help="Reference to Project")
    
    # @api.onchange('projet')
    # def _onchange_projet(self):
        
    #     dataa = self.env['sale.order'].browse(self._context.get('active_ids',[]))

    #     self.projet.devis = [(4, dataa.id)]
      

class Ajouter_projet(models.TransientModel):
		_name = 'ajouter.projet'
		_description = "Ajouter projet"



		projet = fields.Many2one('project.project', string='Projets', required = True)


		def action_add_projet(self):
			dataa = self.env['sale.order'].browse(self._context.get('active_ids',[]))

			dataa.projet = self.projet.id
			self.projet.devis = [(4, dataa.id)]
			self.projet.reference_chantier = dataa.x_reference



class projectttt(models.Model):
    _inherit = 'purchase.order'

    projet =  fields.Many2one('project.project',"Projet",help="Reference to Project")
    
    # @api.onchange('projet')
    # def _onchange_projet(self):
        
    #     dataa = self.env['sale.order'].browse(self._context.get('active_ids',[]))

    #     self.projet.devis = [(4, dataa.id)]
      

class Ajouter_projet_achat(models.TransientModel):
		_name = 'ajouter.projet.achats'
		_description = "Ajouter projet"

		

		projet = fields.Many2one('project.project', string='Projets', required = True)
		
		
		def action_add_projet(self):
			dataa = self.env['purchase.order'].browse(self._context.get('active_ids',[]))

			dataa.projet = self.projet.id
			self.projet.achats = [(4, dataa.id)]






class projectttt(models.Model):
    _inherit = 'account.move'

    projet =  fields.Many2one('project.project',"Projet",help="Reference to Project")
    
    # @api.onchange('projet')
    # def _onchange_projet(self):
        
    #     dataa = self.env['sale.order'].browse(self._context.get('active_ids',[]))

    #     self.projet.devis = [(4, dataa.id)]
      

class Ajouter_projet_achat(models.TransientModel):
		_name = 'ajouter.projet.moves'
		_description = "Ajouter projet"

		

		projet = fields.Many2one('project.project', string='Projets', required = True)
		
		
		def action_add_projet(self):
			dataa = self.env['account.move'].browse(self._context.get('active_ids',[]))

			dataa.projet = self.projet.id
			self.projet.factures = [(4, dataa.id)]





class Ajouter_achats_project(models.TransientModel):
		_name = 'ajouter.achats.projectt'
		_description = "Ajouter projet"

		

		achats = fields.Many2one('purchase.order', string='Achat', required = True)
		
		
		def action_add_projet(self):
			data = self.env['project.project'].browse(self._context.get('active_ids',[]))

			data.achats = [(4, self.achats.id)]
			self.achats.projet = data.id

class Ajouter_factures_project(models.TransientModel):
		_name = 'ajouter.factures.projectt'
		_description = "Ajouter factures"

		

		factures = fields.Many2one('account.move', string='Facture', required = True)
		
		
		def action_add_projet(self):
			data = self.env['project.project'].browse(self._context.get('active_ids',[]))

			data.factures = [(4, self.factures.id)]
			self.factures.projet = data.id


class Ajouter_devis_project(models.TransientModel):
		_name = 'ajouter.devis.projectt'
		_description = "Ajouter devis"

		

		devis = fields.Many2one('sale.order', string='Devis', required = True)
		
		
		def action_add_projet(self):
			data = self.env['project.project'].browse(self._context.get('active_ids',[]))

			data.devis = [(4, self.devis.id)]
			self.devis.projet = data.id
			data.reference_chantier = self.devis.x_reference



class delier_achat_projet(models.TransientModel):
	_name = 'delier.achat.projet'
	_description = "delier Achat"

	
	achat = fields.Many2one('purchase.order', string='Achats', required = True)
	
	

	
	@api.onchange('achat')
	def _getfilter(self):
		data = self.env['project.project'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'achat': [('id', 'in', data.achats.ids)]}}
	def action_delier_achat(self):
		data = self.env['project.project'].browse(self._context.get('active_ids',[]))
		for m in data:
			self.achat.projet = False
			m.achats = [(3, self.achat.id)]



class delier_devis_projet(models.TransientModel):
	_name = 'delier.devis.projet'
	_description = "delier devis"

	
	devis = fields.Many2one('sale.order', string='Devis', required = True)
	
	

	
	@api.onchange('devis')
	def _getfilter(self):
		data = self.env['project.project'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'devis': [('id', 'in', data.devis.ids)]}}
	def action_delier_devis(self):
		data = self.env['project.project'].browse(self._context.get('active_ids',[]))
		for m in data:
			self.devis.projet = False
			m.devis = [(3, self.devis.id)]


class delier_fact_projet(models.TransientModel):
	_name = 'delier.fact.projet'
	_description = "delier fact"

	
	facture = fields.Many2one('account.move', string='facture', required = True)
	
	

	
	@api.onchange('facture')
	def _getfilter(self):
		data = self.env['project.project'].browse(self._context.get('active_ids',[])) 
		return {'domain': {'facture': [('id', 'in', data.factures.ids)]}}
	def action_delier_fact(self):
		data = self.env['project.project'].browse(self._context.get('active_ids',[]))
		for m in data:
			self.facture.projet = False
			m.factures = [(3, self.facture.id)]