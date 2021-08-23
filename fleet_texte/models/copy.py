


from odoo import api, exceptions, fields, models, _

from odoo import api, fields, models, tools


class addchampsfleet(models.Model):
    _inherit = 'fleet.vehicle'

    dkv = fields.Char('N° DKP',store=True,index=True)
    telepeage = fields.Char('N° télépéage',store=True,index=True)
