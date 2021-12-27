# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    export_id = fields.Many2one('account.export.history', copy=False, string="Export")
    compte_tiers = fields.Char(string='Compte tiers', compute="get_compte_tiers")

    def get_compte_tiers(self):
        " return compte tiers"
        customers_labels = ("Recevable",)
        supplier_labels = ("Payable",)
        
        for line in self:
            if line.account_id.user_type_id.name in customers_labels:
                line.compte_tiers = line.partner_id.third_account_customer
            elif line.account_id.user_type_id.name in supplier_labels:
                line.compte_tiers = line.partner_id.third_account_supplier
            else:
                line.compte_tiers = False


