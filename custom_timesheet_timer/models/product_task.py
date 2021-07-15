# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    timesheet_last_time = fields.Char('Timesheet Last Time')

    def action_timer_pause(self):
        res = super(ProjectTask, self).action_timer_pause()
        for task in self:
            task.timesheet_last_time = task.get_task_current_time()
        return res

    def get_task_current_time(self):
        for task in self:
            if task.timesheet_timer_pause:
                diff = task.timesheet_timer_pause - task.timesheet_timer_start
            else:
                diff = datetime.now() - task.timesheet_timer_start
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            current_time_str = '{0}:{1}:{2}'.format(str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2))
            return current_time_str
