# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime

class ProjectTask2(models.Model):
    _inherit = 'project.task'

    def _action_create_timesheet(self, time_spent):
        # return {
        #     "name": _("Confirm Time Spent"),
        #     "type": 'ir.actions.act_window',
        #     "res_model": 'project.task.create.timesheet',
        #     "views": [[False, "form"]],
        #     "target": 'new',
        #     "context": {
        #         **self.env.context,
        #         'active_id': self.id,
        #         'active_model': 'project.task',
        #         'default_time_spent': time_spent,
        #     },
        # }

        # data = self.env['project.task'].browse(self._context.get('active_ids',[]))

        values = {
            'task_id': self.id,
            'project_id': self.project_id.id,
            'date': datetime.now(),
            'name': self.name,
            'user_id': self.env.uid,
            'unit_amount': time_spent,
        }
        self.write({
            'timesheet_timer_start': False,
            'timesheet_timer_pause': False,
            'timesheet_timer_last_stop': fields.datetime.now(),
        })
        return self.env['account.analytic.line'].create(values)
