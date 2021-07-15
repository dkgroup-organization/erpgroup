# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class planningaddTimer(models.Model):
    _inherit = 'planning.slot'

    descriptiontask = fields.Html(string='Description' ,compute='_compute_discriptionn')
    timesheet_timer_start = fields.Datetime("Timesheet Timer Start", compute="_timer_start")
    timesheet_timer_pause = fields.Datetime("Timesheet Timer Last Pause" , compute="_timer_pause")
    total_hours_spent = fields.Float("Total Hours", compute='_compute_total_hours_spent')

    @api.depends('task_id')
    def _compute_discriptionn(self):
      for record in self:
        if record.task_id:
           record.descriptiontask = record.task_id.description
        else:
            record.descriptiontask = False


    @api.depends('task_id')
    def _timer_start(self):
      for record in self:
        if record.task_id:
           record.timesheet_timer_start = record.task_id.timesheet_timer_start
        else:
            record.timesheet_timer_start = False

    @api.depends('task_id')
    def _compute_total_hours_spent(self):
      for record in self:
        if record.task_id:
           record.total_hours_spent = record.task_id.total_hours_spent
        else:
            record.total_hours_spent = False


    @api.depends('task_id')
    def _timer_pause(self):
      for record in self:
        if record.task_id:
           record.timesheet_timer_pause = record.task_id.timesheet_timer_pause
        else:
            record.timesheet_timer_pause= False


    def action_timer_start(self):
      for  record in self:
        if record.task_id:
           return record.task_id.action_timer_start()
        else:
           return False

    def action_timer_pause(self):
      for record in self:
        if record.task_id:
           return record.task_id.action_timer_pause()

        else:
            return False
    def action_timer_resume(self):
      for record in self:
        if record.task_id:
           return record.task_id.action_timer_resume()
        else:
            return False

    def action_timer_stop(self):
      for record in self:
        if record.task_id:
           return record.task_id.action_timer_stop()
        else:
           return False


