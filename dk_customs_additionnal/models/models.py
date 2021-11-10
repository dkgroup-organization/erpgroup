# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dk_customs_additionnal(models.Model):
    _inherit = 'res.partner'

    third_account_customer = fields.Many2one('account.account', string='compte tiers client')
    third_account_supplier = fields.Many2one('account.account', string='compte tiers fournisseur')


class dk_customs_additionnal(models.Model):
    _inherit = 'account.move.line'
#
    compte_tiers  =fields.Many2one('account.account', string='compte tiers client',compute="get_compte_tiers")
#
#
    def get_compte_tiers(self):
<<<<<<< Updated upstream
        if self.account_id.user_type_id.name == "Recevable":
=======
        customers_labels = ("Recevable",)
        supplier_labels = ("Payable",)

        if self.account_id.user_type_id.name in customers_labels:
>>>>>>> Stashed changes
            self.compte_tiers = self.partner_id.third_account_customer
        elif self.account_id.user_type_id.name == "Payable":
            self.compte_tiers = self.partner_id.third_account_supplier
        else:
            self.compte_tiers = None
