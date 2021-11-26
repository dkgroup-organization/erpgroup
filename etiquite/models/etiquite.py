




from odoo import api, fields, models, tools, SUPERUSER_ID, _


class etiquite(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many('project.tags', string='testtt',required=True)
    project_id = fields.Many2one('project.project', string='Project yyyy',
        compute='_compute_project_id', store=True, readonly=True,
        index=True, tracking=True, check_company=True, change_default=True)
