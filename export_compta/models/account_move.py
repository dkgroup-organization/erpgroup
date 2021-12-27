# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    export_id = fields.Many2one('account.export.history', copy=False, string="Export")

    def button_unlink_export(self):
        "unlink previous link to export history"
        for move in self:
            move.export_id = False



