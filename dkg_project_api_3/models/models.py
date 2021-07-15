# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
import datetime
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = ["project.task"]

    
    def get_timer(self):
        for data in self:
            if data.timesheet_timer_start:
                timer = datetime.datetime.now() - data.timesheet_timer_start
            else:
                timer = False
        return timer


