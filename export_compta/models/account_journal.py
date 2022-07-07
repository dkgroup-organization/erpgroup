# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    export_code2 = fields.Char("CEGID code 2 character")
    export_code3 = fields.Char("CEGID code 3 character")




