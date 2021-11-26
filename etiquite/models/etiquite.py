




from odoo import api, fields, models, tools, SUPERUSER_ID, _


class etiquite(models.Model):
    _inherit = 'project.task'

    sequence = fields.Integer(string='Sequence', index=True, default=10,
        help="Gives the sequence order when displaying a list of tasks.")
