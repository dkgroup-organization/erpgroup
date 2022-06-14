# Copyright 2016-2020 Onestein (<http://www.onestein.eu>)
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from datetime import timedelta, datetime
import markupsafe
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    # Used by PERT
    date_earliest_start = fields.Datetime("date_earliest_start")
    date_earliest_end = fields.Datetime("date_earliest_end")
    date_latest_start = fields.Datetime("date_latest_start")
    date_latest_end = fields.Datetime("date_latest_end")
    date_manual_start = fields.Datetime("date_manual_start")
    date_manual_end = fields.Datetime("date_manual_end")

    checking_error = fields.Selection([('none', 'None'), ('timesheet', 'Timesheet')], string="error", default="none")

    # Used by PERT, calendar deadline
    date_fixed = fields.Boolean('Fixed date')

    # Used By gantt, computing date date_planned_start
    #planned_date_begin, date_planned_start
    planned_date_begin = fields.Datetime("Date planned start",
                                         compute="get_date_planned_start",
                                         inverse="set_date_planned_start")
    #planned_date_end, date_planned_finished
    planned_date_end = fields.Datetime("Date planned finished",
                                            compute="get_date_planned_finished",
                                            inverse="set_date_planned_finished")

    date_planned_delay = fields.Float("Planned delay", compute="get_date_planned_delay")
    date_planned_slack = fields.Float("Planned delay")

    # validation user
    validation_user_id = fields.Many2one("res.users", "Validator")

    dependency_task_ids = fields.Many2many(
        string="Dependencies",
        comodel_name="project.task",
        relation="project_task_dependency",
        column1="task_id",
        column2="dependency_task_id",
    )

    stage_state = fields.Selection(related="stage_id.state", store=True)
    timeline_description = fields.Html('Gantt description', compute='get_timeline_description')

    def get_timeline_description(self):
        """ Create HTML description for the timeline gantt"""
        for task in self:
            html_description = '<td>planned: %d</td>' % task.planned_hours
            html_description += '<td>working: %d</td>' % task.effective_hours

            task.timeline_description = markupsafe.Markup(html_description)

    @api.model
    def button_update_date(self):
        """ Update the date planned"""
        active_id = self.env.context.get('active_id')
        if active_id:
            task = self.browse(int(active_id))
            task.get_date_planned_finished()
            task.get_date_planned_start()

    def get_date_planned_delay(self):
        """ define """
        for task in self:
            planned_hours = task.planned_hours or 0.0
            timesheet_hours = 0.0

            for timesheet in task.timesheet_ids:
                timesheet_hours += timesheet.unit_amount or 0.0
            # result by planned and timesheet
            if timesheet_hours > planned_hours:
                task.date_planned_delay = timesheet_hours
            else:
                task.date_planned_delay = planned_hours
            if not task.date_planned_delay:
                task.date_planned_delay = 1.0

    def get_date_planned_start(self):
        """ define the date start on the gantt:
        Use hr_timesheet"""
        for task in self:
            timesheet_date_ids = self.env['account.analytic.line'].search(
                [('task_id', '=', task.id)], order='date asc')
            if timesheet_date_ids:
                timesheet_date = timesheet_date_ids[0].date
                timesheet_datetime = datetime(
                    year=timesheet_date.year,
                    month=timesheet_date.month,
                    day=timesheet_date.day,
                    hour=8,
                )
            else:
                timesheet_datetime = False

            if task.start_datetime:
                if task.date_fixed:
                    task.planned_date_begin = task.start_datetime
                elif timesheet_datetime and timesheet_datetime < task.start_datetime:
                    task.planned_date_begin = timesheet_date
                else:
                    task.planned_date_begin = task.start_datetime
            elif timesheet_datetime:
                task.planned_date_begin = timesheet_datetime
            elif task.date_manual_start:
                task.planned_date_begin = task.date_manual_start
            elif task.date_assign:
                task.planned_date_begin = task.date_assign
            else:
                task.planned_date_begin = fields.Datetime.now()

            if hasattr(task, 'planns'):
                "enterprise version"
                now = fields.Datetime.now()
                for line in task.planns:
                    if now < line.start_datetime < task.planned_date_begin:
                        task.planned_date_begin = line.start_datetime

            if not task.planned_date_begin:
                task.planned_date_begin = fields.Datetime.now()

    def set_date_planned_start(self):
        """ define the date start on the gantt:
        Use hr_timesheet"""
        for task in self:
            task.date_manual_start = task.planned_date_begin
            task.start_datetime = task.planned_date_begin

    def get_date_planned_finished(self):
        """ define the date start on the gantt:
        Use hr_timesheet"""
        for task in self:
            timesheet_date_ids = self.env['account.analytic.line'].search(
                [('task_id', '=', task.id)], order='date desc')
            if timesheet_date_ids:
                timesheet_date = timesheet_date_ids[0].date
                # by default start at 8 am
                hours = int(8.0 + (timesheet_date_ids[0].unit_amount or 1.0))
                if hours > 22:
                    hours = 22
                    task.checking_error = "timesheet"
                if hours < 0:
                    hours = 0
                    task.checking_error = "timesheet"

                timesheet_datetime = datetime(
                    year=timesheet_date.year,
                    month=timesheet_date.month,
                    day=timesheet_date.day,
                    hour=hours,
                )
            else:
                timesheet_datetime = False

            if task.end_datetime:
                if task.date_fixed:
                    task.planned_date_end = task.end_datetime
                elif timesheet_datetime and timesheet_datetime > task.end_datetime:
                    task.planned_date_end = timesheet_datetime
                else:
                    task.planned_date_end = task.end_datetime
            elif timesheet_datetime:
                task.planned_date_end = timesheet_datetime
            elif task.date_manual_end:
                task.planned_date_end = task.date_manual_end
            elif task.date_deadline:
                task.planned_date_end = task.date_deadline
            else:
                hours = task.planned_hours or 1.0
                task.planned_date_end = (task.planned_date_begin or fields.Datetime.now()) + timedelta(hours=int(hours))

            if hasattr(task, 'planns'):
                "enterprise version"
                now = fields.Datetime.now()
                for line in task.planns:
                    if line.end_datetime > now and line.end_datetime > task.planned_date_end:
                        task.planned_date_end = line.end_datetime

    def set_date_planned_finished(self):
        """ define the date end on the gantt:
        Use hr_timesheet"""
        for task in self:
            _logger.info("\n---set_date_planned_finished-----: %s %s" % (task, task.planned_date_end))
            task.date_manual_end = task.planned_date_end
            task.end_datetime = task.planned_date_end
            task.get_date_planned_finished()

    def update_date(self):
        """ Update the date planned"""
        self.get_date_planned_finished()
        self.get_date_planned_start()