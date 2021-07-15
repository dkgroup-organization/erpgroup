# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import fields,models

class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_config = fields.Many2one('pos.config', string='Point de Vente', domain=[('active', '=', True)])