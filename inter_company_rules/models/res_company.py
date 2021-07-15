# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import Warning


class res_company(models.Model):

    _inherit = 'res.company'

    so_from_po = fields.Boolean(string="Créer des commandes de vente lors de l\'achat à cette société",
        help="Générer une commande de vente lors de la création d'une commande avec cette société en tant que fournisseur. \n L'utilisateur intersociétés doit au moins être un utilisateur de vente..")
    po_from_so = fields.Boolean(string="Créer des bons de commande d\'achat lors de la vente à cette société",
        help="Générer une commande d\'achat lors de la création d\'une commande avec cette société en tant que client.")
    auto_generate_invoices = fields.Boolean(string="Créer une facture / remboursement lors de l\'encodage de facture / remboursement",
        help="Générer des factures client / fournisseur (et remboursements) lors du codage des factures (ou remboursements) faites à cette société. \n exemple: générer une facture client lors de la création d'une facture avec cette société en tant que fournisseur.")
    auto_validation = fields.Boolean(string="Validation automatique des commandes d'achat / vente",
        help="Lorsqu'une commande d\'achat ou une commande de vente est créé par un règle, il sera automatiquement validé.")
    intercompany_user_id = fields.Many2one("res.users", string="Utilisateur inter-sociétés", default=SUPERUSER_ID,
        help="Utilisateur responsable de la création de documents déclenchée par des règles intersociétés.")
    warehouse_id = fields.Many2one("stock.warehouse", string="Entrepôt",
        help="Valeur par défaut à définir sur les commandes d'achat (ventes) qui seront créées en fonction des commandes de vente (commandes d'achat) passées à cette société")

    @api.model
    def _find_company_from_partner(self, partner_id):
        company = self.sudo().search([('partner_id', '=', partner_id)], limit=1)
        return company or False

    @api.one
    @api.constrains('po_from_so', 'so_from_po', 'auto_generate_invoices')
    def _check_intercompany_missmatch_selection(self):
        if (self.po_from_so or self.so_from_po) and self.auto_generate_invoices:
            raise Warning(_('''Vous ne pouvez pas choisir de créer des factures basées sur d'autres factures
                    simultanément avec une autre option ('Créer des ordres de vente lors de l'achat de cette
                    société "ou" Créer des bons de commande lors de la vente à cette société')!'''))

