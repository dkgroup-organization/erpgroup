# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class acompte(models.Model):
    _inherit = 'account.move'

  
    due = fields.Float(string='Amount Due',store=True, help="Remaining amount due." )
