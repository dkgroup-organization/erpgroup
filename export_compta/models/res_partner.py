# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    third_account_customer = fields.Char(string='compte tiers client')
    third_account_supplier = fields.Char(string='compte tiers fournisseur')


