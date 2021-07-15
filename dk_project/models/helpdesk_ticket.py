# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    timesheet_timer_start = fields.Datetime("Timesheet Timer Start", related="task_id.timesheet_timer_start")
    timesheet_timer_pause = fields.Datetime("Timesheet Timer Last Pause",
                                            related="task_id.timesheet_timer_pause")
    timesheet_timer_first_start = fields.Datetime("Timesheet Timer First Use", readonly=True,
                                                  related="task_id.timesheet_timer_first_start")
    timesheet_timer_last_stop = fields.Datetime("Timesheet Timer Last Use", readonly=True,
                                                related="task_id.timesheet_timer_last_stop")
    display_timesheet_timer = fields.Boolean("Display Timesheet Time", related="task_id.display_timesheet_timer")
    allow_billable = fields.Boolean(related="task_id.project_id.allow_billable")
    total_hours_spent = fields.Float("Total Hours", related="task_id.total_hours_spent")

    def action_timer_start(self):
        self.ensure_one()
        return self.task_id.action_timer_start()

    def action_timer_pause(self):
        self.ensure_one()
        self.task_id.action_timer_pause()

    def action_timer_resume(self):
        self.ensure_one()
        self.task_id.action_timer_resume()

    def action_timer_stop(self):
        self.ensure_one()
        action_stop = self.task_id.action_timer_stop()
        if isinstance(action_stop, dict) and action_stop.get('context'):
            action_stop['context']['helpdesk_ticket_id'] = self.id
        return action_stop
