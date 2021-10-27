# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime

class planning_display(models.Model):
    _inherit = "planning.slot"
    
    display_name = fields.Char(
        string='display name',
        compute='_compute_display')
    
    
   


    @api.depends('employee_id','project_id','role_id')
    def _compute_display(self):
        for var in self:
             var.display_name=  str(var.employee_id.name) +"\n   #ROLE:"+str(var.role_id.name)+"\n   #PROJET:"+str(var.project_id.name) + "\n  #TÄCHE:"+ str(var.task_id.name)
