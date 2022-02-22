from odoo import api, fields, models, _
from odoo.exceptions import ValidationError,UserError


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    stage_lead_id = fields.Many2one(
        'crm.stage', string='Stage', index=True, tracking=True,
        ondelete='restrict',
        domain="['|', ('stage_lead', '=', True)]")




