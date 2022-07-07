# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    export_id = fields.Many2one('account.export.history', copy=False, string="Export")
    compte_tiers = fields.Char(string='Compte tiers', compute="get_compte_tiers")

    def get_compte_tiers(self):
        """ return compte tiers"""
        for line in self:
            partner = line.partner_id
            if line.account_id.user_type_id.type == "receivable":
                if not line.partner_id.third_account_customer and line.partner_id.parent_id:
                    partner = line.partner_id.parent_id
                line.compte_tiers = partner.third_account_customer or '?'

            elif line.account_id.user_type_id.type == "payable":
                if not line.partner_id.third_account_supplier and line.partner_id.parent_id:
                    partner = line.partner_id.parent_id
                line.compte_tiers = partner.third_account_supplier or '?'

            else:
                line.compte_tiers = False


