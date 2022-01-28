# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class task_task_limite(models.Model):
    _inherit = 'project.task'

    date_deadline = fields.Datetime(string='Deadline', index=True, copy=False, tracking=True)

