# Copyright 2018-2020 Onestein
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from datetime import timedelta


class ProjectProject(models.Model):
    _inherit = "project.project"

    timeline_show = fields.Boolean('Show in timeline', default=True)
    gantt_methode = fields.Selection([('asap', 'As speed as possible'), ('jit', 'Just in time')],
                    default='asap', string="Plan method")


    def view_all_timeline_task(self):
        """ Use filter timeline_show"""
        condition = [('project_id', 'in', self.ids)]
        task_ids = self.env['project.task'].search(condition)
        if task_ids:
            task_ids.timeline_show = True

    def hide_old_timeline_task(self):
        """ Use filter timeline_show"""
        # 2 months old task to hide
        now_2month_old = fields.Datetime.now() - timedelta(weeks=8)

        for project in self:
            condition = [('project_id', '=', project.id)]
            timeline_show = False
            for task in self.env['project.task'].search(condition):
                if task.planned_date_begin < now_2month_old and task.planned_date_end < now_2month_old:
                    task.timeline_show = False
                else:
                    task.timeline_show = True
                    timeline_show = True

            project.timeline_show = timeline_show

    def plan_task(self):
        """ plan the project """
        # define the number of computing time step by dependency
        # The dictionnary
        def all_step(time_step, task_ids):
            """ define the number of time step computing """
            independent_task_ids = self.env['project.task'].search(
                [('id', '=', task_ids.ids), ('dependency_ids', '=', False)])

            child_task_ids = self.env['project.task'].search(
                [('id', '=', task_ids.ids), ('parent_id', '!=', False)])





    @api.model
    def cron_project(self):
        """ Update project configuration"""
        condition = []
        for poject in self.search(condition):
            poject.hide_old_timeline_task

