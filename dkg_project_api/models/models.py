# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = ["project.task"]

    #task_adresse = fields.Char(string="", required=False, )
    localisation = fields.Char('Localisation Axes', copy=False, help="Example 33.578921, -7.616295")
    #google_map_long = fields.Char(string="", required=False, )
    #google_map_lat = fields.Char(string="", required=False, )
    planns = fields.Many2many(comodel_name="planning.slot", string="Plans", )
    pieces_joint = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

#    @api.depends('project_id', 'project_id.tag_ids')
#    def _compute_tag_ids(self):
#        for rec in self:
#            if rec.project_id.tag_ids:
#                rec.tag_ids = rec.project_id.tag_ids

    tag_ids = fields.Many2many(comodel_name="project.tags", string="Tags", related='project_id.tag_ids',
    				#compute="_compute_tag_ids"
    				)
            
    """
    in_active_week = fields.Boolean(string="In Active Week ?", compute='_compute_in_active_week' )

    @api.depends('end_datetime')
    def in_active_week(self):
        today = fields.Datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = today + timedelta(days=6)

        if self.end_datetime and self.end_datetime >= week_start and self.end_datetime <= week_end:
            self.in_active_week == True
     """       

    @api.depends('planns')
    def _compute_start_datetime(self):
        #reports = self.env['planning.slot'].search([('company_id', '=', self.company_data['company'].id)], order='price_subtotal DESC')
        for record in self:
            dates = []  # Declaring empty array
            if record.planns:
                for plan in record['planns']:  # foreach plan in task
                    #			if plan:  # if we have a plan
                    dates.append(plan.start_datetime)  # Add it to the array
                    record['start_datetime'] = min(dates)  # Get the max from that array

    start_datetime = fields.Datetime(string="Start Date Time", required=False,
                                     compute='_compute_start_datetime',
                                     store = True
                                     )

    @api.depends('planns')
    def _compute_end_datetime(self):

        for record in self:
            dates = []  # Declaring empty array
            if record.planns:
                for plan in record['planns']:  # foreach plan in task
                    #			if plan:  # if we have a plan
                    dates.append(plan.end_datetime)  # Add it to the array
                    record['end_datetime'] = max(dates)  # Get the max from that array
                    

    end_datetime = fields.Datetime(string="End Date Time", required=False,
                                   compute='_compute_end_datetime',
                                   store = True
                                    )
                                 

class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_finish_stage = fields.Boolean(string="Is Finish Stage")

class ProjectProject(models.Model):
    _inherit = "project.project"

    reference_chantier = fields.Char(string="Chantier Ref")
