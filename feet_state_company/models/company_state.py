from odoo import api, exceptions, fields, models, _

class status(models.Model):
    _inherit = 'fleet.vehicle.state'

    company_id = fields.Many2one(
        'res.company', 'Company',
        # default=lambda self: self.env.company,
    )