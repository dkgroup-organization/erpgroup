from odoo import api, exceptions, fields, models, _
from odoo.exceptions import ValidationError

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'



    contact_client = fields.Many2many('res.partner','account_move_res_partner_client_rel',string="Contact client")
    pv_livraison_30k = fields.Binary( string="PV de livraison")
    pv_livraison_30k_filename = fields.Char( string="PV de livraison")
    bon_commande_30k = fields.Binary(string="Bon de commande")
    bon_commande_30k_filename= fields.Char( string="PV de livraison")
    accord_mail_30k = fields.Binary(string="Accord Mail")
    accord_mail_30k_filename= fields.Char( string="PV de livraison")

    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        if self.amount_total >= 30000:
            if not self.pv_livraison_30k:
                raise ValidationError("PV de livraison Requis pour les factures de plus de 30.000, voir onglet Pièces Jointe")
            if not self.bon_commande_30k:
                raise ValidationError("Bon de commande Requis pour les factures de plus de 30.000, voir onglet Pièces Jointe")
            if not self.accord_mail_30k:
                raise ValidationError("Accord mail  Requis pour les factures de plus de 30.000, voir onglet Pièces Jointe")
        return res

