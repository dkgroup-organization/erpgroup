# -*- coding: utf-8 -*-
from odoo import models, fields, api

class inter_company_rules_configuration(models.TransientModel):

    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Sélectionner une société',
        help='Sélectionner une société pour configurer les règles inter-sociétés.')
    rule_type = fields.Selection([('so_and_po', 'Paramètre Ventes et Achats pour inter sociétés'),
        ('invoice_and_refunds', 'Créer une facture / remboursement lors de l\'encodage de facture / remboursement')],
        help='Sélectionnez le type de configuration des règles inter-sociétés dans la société sélectionnée..')
    so_from_po = fields.Boolean(string='Créer des commandes de vente lors de l\'achat à cette société',
        help='Générer une commande de vente lors de la création d\'une commande d\'achat avec cette société en tant que fournisseur.')
    po_from_so = fields.Boolean(string='Créer des bons de commande d\'achat lors de la vente à cette société',
        help='Générer une commande d\'achat lors de la création d\'une commande avec cette société en tant que client.')
    auto_validation = fields.Boolean(string='Validation automatique des commandes d\'achat / vente',
        help='''Lorsqu'une commande d\'achat ou une commande de vente est créé par un
            règle, il sera automatiquement validé.''')
    warehouse_id = fields.Many2one('stock.warehouse', string='Entrepôt pour les commandes d\'achat',
        help='Valeur par défaut à définir sur les commandes d\'achat qui seront créées en fonction des commandes de vente passées à cette société.')

    @api.onchange('rule_type')
    def onchange_rule_type(self):
        if self.rule_type == 'so_and_po':
            self.invoice_and_refunds = False

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            rule_type = False
            if self.company_id.so_from_po or self.company_id.po_from_so or self.company_id.auto_validation:
                rule_type = 'so_and_po'
            elif self.company_id.auto_generate_invoices:
                rule_type = 'invoice_and_refunds'

            self.rule_type = rule_type
            self.so_from_po = self.company_id.so_from_po
            self.po_from_so = self.company_id.po_from_so
            self.auto_validation = self.company_id.auto_validation
            self.warehouse_id = self.company_id.warehouse_id.id

    def set_inter_company_configuration(self):
        if self.company_id:
            vals = {
                'so_from_po': self.so_from_po if self.rule_type == 'so_and_po' else False,
                'po_from_so': self.po_from_so if self.rule_type == 'so_and_po' else False,
                'auto_validation': self.auto_validation if self.rule_type == 'so_and_po' else False,
                'auto_generate_invoices': True if self.rule_type == 'invoice_and_refunds' else False,
                'warehouse_id': self.warehouse_id.id
            }
            self.company_id.write(vals)
