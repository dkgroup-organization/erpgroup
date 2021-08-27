# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class allow_invoicing(models.Model):
    _inherit = 'res.partner'

    allow_invoicing = fields.Boolean('Permettre la facturation pour ce Client', help='Permettre la facturation',default=False)
    bcd_exige = fields.Boolean('N° de BDC exigé', help='N° de BDC exigé dans la facture',default=False)

    montant_garantie = fields.Float(string='Montant de garantie ',default=0.0 ,help='montant de garantie qui est transmis par notre factor')


class allow_facturation(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
            raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))

        if (self.type in ('out_invoice','out_refund') and self.partner_id.allow_invoicing == False):
            raise UserError(_("vous n'avez pas le droit de facturation pour ce client, veuillez contacter le comptable pour verifier les informations du client"))
        return self.post()


