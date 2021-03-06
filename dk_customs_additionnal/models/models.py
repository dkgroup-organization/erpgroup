# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import AccessError, UserError, ValidationError
class dk_customs_additionnal(models.Model):
    _inherit = 'res.partner'

    third_account_customer = fields.Char(string='compte tiers client')
    third_account_supplier = fields.Char(string='compte tiers fournisseur')


class dk_customs_additionnal(models.Model):
    _inherit = 'account.move.line'
#
    compte_tiers  =fields.Char(string='compte tiers client',compute="get_compte_tiers_old")
#
    def get_compte_tiers_old(self):
        customers_labels = ("Recevable", )
        supplier_labels = ("Payable",)

        if self.account_id.user_type_id.name in customers_labels:
            self.compte_tiers = self.partner_id.third_account_customer
        elif self.account_id.user_type_id.name in supplier_labels:
            self.compte_tiers = self.partner_id.third_account_supplier
        else:
            self.compte_tiers = None



