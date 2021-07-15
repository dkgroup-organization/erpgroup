# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime

class ProjectTask(models.Model):
    _inherit = ["project.task"]

    start_datetime = fields.Datetime(string="Start Date Time", required=False,
                                     compute='_compute_start_datetime',store=False)
    end_datetime = fields.Datetime(string="End Date Time", required=False,
                                   compute='_compute_end_datetime',stroe=False)
