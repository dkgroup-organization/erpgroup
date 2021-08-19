# -*- coding: utf-8 -*-
#
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    factures_fournisseur = fields.Many2many("account.move",'sale_order_move_rel_fourniseur',string="Factures",domain = "[('move_type','=','	in_invoice')]")
    list_article_achat = fields.Many2many('purchase.order.line','project_project_purchase_order_line_rel',string="Liste des articles",compute="_get_article_achat")
    list_article_devis = fields.Many2many('sale.order.line','project_project_sale_order_line_rel',string="Liste des articles",compute="_get_article_devis")
    list_article_facture = fields.Many2many('account.move.line','project_project_account_move_line_rel',string="Liste des articles",compute="_get_article_facture")

    @api.depends('devis')
    def _get_article_devis(self):
        for rec in self:
            list = rec.devis.mapped('order_line').ids
            #            list+=rec.factures.mapped('invoice_line_ids').mapped('product_id').ids
            #            raise ValidationError(type(list))
            rec.list_article_devis = [(6, 0, list)]
        return True

    @api.depends('factures', 'factures_fournisseur')
    def _get_article_facture(self):
        for rec in self:
            list = rec.factures_fournisseur.mapped('invoice_line_ids').ids
            list += rec.factures.mapped('invoice_line_ids').ids
            rec.list_article_facture = [(6, 0, list)]
        return True

    @api.depends('achats')
    def _get_article_achat(self):
        for rec in self:
            list = rec.achats.mapped('order_line').ids
            rec.list_article_achat=[(6, 0, list)]
        return True





