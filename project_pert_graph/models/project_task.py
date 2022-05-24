# Copyright 2016-2020 Onestein (<http://www.onestein.eu>)
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    # Used by PERT
    date_earliest_start = fields.Datetime("Date")
    date_earliest_end = fields.Datetime("Date")
    date_latest_start = fields.Datetime("Date")
    date_latest_end = fields.Datetime("Date")
    date_manual_start = fields.Datetime("Date")
    date_manual_end = fields.Datetime("Date")

    # Used by PERT, calendar deadline
    date_fixed = fields.Boolean('Fixed date')

    # Used By gantt, computing date date_planned_start
    date_planned_start = fields.Datetime("Date planned start",
                                         compute="get_date_planned_start",
                                         inverse="set_date_planned_start")

    date_planned_finished = fields.Datetime("Date planned finished",
                                            compute="get_date_planned_finished",
                                            inverse="set_date_planned_finished")

    date_planned_delay = fields.Float("Planned delay", compute="get_date_planned_delay")
    date_planned_slack = fields.Float("Planned delay")

    # validation user
    validation_user_id = fields.Many2one("res.users", "Validator")

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
                    task.date_planned_start = task.start_datetime
                elif timesheet_datetime and timesheet_datetime < task.start_datetime:
                    task.date_planned_start = timesheet_date
                else:
                    task.date_planned_start = task.start_datetime
            elif timesheet_datetime:
                task.date_planned_start = timesheet_datetime
            elif task.date_manual_start:
                task.date_planned_start = task.date_manual_start
            elif task.date_assign:
                task.date_planned_start = task.date_assign
            else:
                task.date_planned_start = task.create_date

    def set_date_planned_start(self):
        """ define the date start on the gantt:
        Use hr_timesheet"""
        _logger.info("\n%s" % self.env.context)
        for task in self:
            _logger.info("\n--------: %s %s" % (task, task.date_planned_start))

            task.manual_start_date = task.date_planned_start

    def get_date_planned_finished(self):
        """ define the date start on the gantt:
        Use hr_timesheet"""
        for task in self:
            timesheet_date_ids = self.env['account.analytic.line'].search(
                [('task_id', '=', task.id)], order='date desc')
            if timesheet_date_ids:
                hours = int(8.0 + (task.date_planned_delay or 0.0))

                timesheet_date = timesheet_date_ids[0].date
                hours = int(8.0 + (timesheet_date_ids[0].unit_amount or 1.0))
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
                    task.date_planned_finished = task.end_datetime
                elif timesheet_datetime and timesheet_datetime > task.end_datetime:
                    task.date_planned_finished = timesheet_datetime
                else:
                    task.date_planned_finished = task.end_datetime
            elif timesheet_datetime:
                task.date_planned_finished = timesheet_datetime
            elif task.date_manual_end:
                task.date_planned_finished = task.date_manual_end
            elif task.date_deadline:
                task.date_planned_finished = task.date_deadline
            else:
                task.date_planned_finished = task.create_date + timedelta(hours=1)

    def set_date_planned_finished(self):
        """ define the date end on the gantt:
        Use hr_timesheet"""
        for task in self:
            _logger.info("\n---set_date_planned_finished-----: %s %s" % (task, task.date_planned_finished))
            task.manual_end_date = task.date_planned_finished
