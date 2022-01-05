

from odoo import fields, models, api, _




class partner(models.Model):
    _inherit = 'res.partner'

    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)









