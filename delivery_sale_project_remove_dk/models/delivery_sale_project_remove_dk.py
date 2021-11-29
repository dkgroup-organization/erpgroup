from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

import logging
_logger = logging.getLogger(__name__)

class delivery_sale_project_remove_dk_inherited(models.Model):
    _inherit = 'purchase.order'


    def action_delier_achat(self):
        data = self.env['purchase.order'].search([("id", "=", self.id)])
        
        self.projet.achats = [(3, self.id)]
        self.projet = False

class delivery_facture_project_remove_dk_inherited(models.Model):
    _inherit = 'account.move'

    def action_delier_account(self):
        data = self.env['account.move'].search([("id", "=", self.id)])
        self.projet.factures = [(3, self.id)]
        self.projet = False

class delivery_vende_project_remove_dk_inherited(models.Model):
    _inherit = 'sale.order'

    def action_delier_sale(self):
        data = self.env['sale.order'].search([("id", "=", self.id)])
        self.projet.devis = [(3, self.id)]
        self.projet = False









