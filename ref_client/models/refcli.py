# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class refcli(models.Model):
    _inherit = 'sale.order'

  
    ref_client = fields.Char(string='Ref.Client',store=True )


class refcli(models.Model):
    _inherit = 'account.move'

  
    ref_client = fields.Char(string='Ref.Client',store=True )
