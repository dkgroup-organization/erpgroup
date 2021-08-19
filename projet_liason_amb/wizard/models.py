# -*- coding: utf-8 -*-
#

from odoo import api, fields, models, _

class AjouterFacturesProjectInherit(models.TransientModel):
    _inherit = 'ajouter.factures.projectt'

    def action_add_projet_fournisseur(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))

        data.factures_fournisseur = [(4, self.factures.id)]
        self.factures.projet = data.id

class DelierFactProjetInherit(models.TransientModel):
    _inherit = 'delier.fact.projet'

    @api.model
    def _getfilter(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        return [('id', 'in', data.factures_fournisseur.ids)]


    facture_fournisseur = fields.Many2one('account.move', string='facture', required=True,domain=_getfilter)


    def action_delier_fact_fournisseur(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        for m in data:
            self.facture.projet = False
            m.factures_fournisseur = [(3, self.facture.id)]