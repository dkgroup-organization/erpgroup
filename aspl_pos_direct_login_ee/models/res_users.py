# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models, api


class res_users(models.Model):
    _inherit = 'res.users'

    login_with_pos_screen = fields.Boolean(string="Login with Direct POS")
    default_pos = fields.Many2one('pos.config',string="POS Config")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: