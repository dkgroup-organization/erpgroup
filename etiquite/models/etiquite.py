





from odoo import api, exceptions, fields, models, _

class acompte(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many('project.tags', string='test',domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
