# Copyright 2014 Daniel Reis
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models



class ProjectTaskDependency(models.Model):
    """Added dependency relation between tasks."""

    _name = "project.task.dependency"
    _description = "Dependency relation "

    task_id = fields.Many2one("project.task", string="Task")
    dependency_task_id = fields.Many2one("project.task", string="Depending task")
    relation_type = fields.Selection([
        ("0", "Finish to Start"),
        ("1", "Start to Start"),
        ("2", "Finish to Finish"),
        ("3", "Start to Finish")
    ], default="0")