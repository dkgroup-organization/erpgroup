# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime


class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = 'project.task.create.timesheet'
    helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket', "Helpdesk Ticket",
        default=lambda self: self.env.context.get('helpdesk_ticket_id', None)
    )

    def save_timesheet(self):
        analytic_line = super(ProjectTaskCreateTimesheet, self).save_timesheet()
        if analytic_line and self.helpdesk_ticket_id:
            analytic_line.write({'helpdesk_ticket_id': self.helpdesk_ticket_id.id})
        # values = {
        #     'task_id': self.task_id.id,
        #     'project_id': self.task_id.project_id.id,
        #     'date': fields.Date.context_today(self),
        #     'name': self.description,
        #     'user_id': self.env.uid,
        #     'unit_amount': self.time_spent,
        # }
        # self.task_id.user_timer_id.unlink()
        # return self.env['account.analytic.line'].create(values)
        return analytic_line
