

from odoo import fields, models, api, _




class account(models.Model):
    _inherit = 'account.move'

    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)









