# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dk_helper_AttestationSimplfiee(models.Model):
    _inherit = 'res.partner'

    is_manager  = fields.Boolean(string="Is Manager?")


