# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dkgroup_custumizations(models.Model):
    _inherit = 'account.move'

    x_contact = fields.Many2one('res.partner',
        ondelete='set null', string="Contact Fournisseur", index=True)

