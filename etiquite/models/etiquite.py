




from odoo import api, fields, models, tools, SUPERUSER_ID, _


class etiquite(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many('project.tags', string='testtt')
