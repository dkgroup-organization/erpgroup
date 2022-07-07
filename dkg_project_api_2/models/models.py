# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, datetime

import logging
_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = "project.project"

    #reference_chantier = fields.Char(string="Chantier Ref")
    add_chantier = fields.Char(string="Addresse Chantier")

class ProjectTask(models.Model):
    _inherit = ["project.task"]

    task_adresse = fields.Char(string="Adresse de la Tâche", required=False, )
    localisation = fields.Char('Localisation Axes', copy=False, help="Example 33.578921, -7.616295")
    google_map_long = fields.Char(string="", required=False, )
    google_map_lat = fields.Char(string="", required=False, )

    # planns = fields.Many2many(comodel_name="planning.slot", string="Plans", )
    # pieces_joint = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    #    @api.depends('project_id', 'project_id.tag_ids')
    #    def _compute_tag_ids(self):
    #        for rec in self:
    #            if rec.project_id.tag_ids:
    #                rec.tag_ids = rec.project_id.tag_ids

    tag_ids = fields.Many2many(comodel_name="project.tags", string="Tags", related='project_id.tag_ids')
    #compute="_compute_tag_ids")



    @api.depends('planns.start_datetime')
    def _compute_start_datetime(self):
        #reports = self.env['planning.slot'].search([('company_id', '=', self.company_data['company'].id)], order='price_subtotal DESC')
        for record in self:
            dates = []  # Declaring empty array
            if record.planns:
                for plan in record['planns']:  # foreach plan in task
                    #			if plan:  # if we have a plan
                    dates.append(plan.start_datetime)  # Add it to the array
                    record['start_datetime'] = min(dates)  # Get the max from that array
            # else:
            #         record['start_datetime'] = False

    start_datetime = fields.Datetime(string="Start Date Time", required=False,
                                     compute='_compute_start_datetime',
                                     store = False
                                     )

    @api.depends('planns.end_datetime')
    def _compute_end_datetime(self):

        for record in self:
            dates = []  # Declaring empty array
            if record.planns:
                for plan in record['planns']:  # foreach plan in task
                    #			if plan:  # if we have a plan
                    dates.append(plan.end_datetime)  # Add it to the array
                    record['end_datetime'] = max(dates)  # Get the max from that array
            # else:
            #     record['end_datetime'] = False
                    

    end_datetime = fields.Datetime(string="End Date Time", required=False,
                                   compute='_compute_end_datetime',
                                   store = False
                                    )

    def list_active_task_by_interval(self, p_start_datetime, p_end_datetime):
        str_object = datetime.strptime(p_start_datetime, "%m-%d-%Y %H:%M:%S")
        end_object = datetime.strptime(p_end_datetime, "%m-%d-%Y %H:%M:%S")
        emp = self.env['hr.employee'].search([('user_id','=', self.env.uid)])

        lst1 = []
        lst2 = []
        lst3 = []
        dicta = {}
        planns_ids = self.env['project.task'].search([]).planns.filtered(lambda r: (r.start_datetime >= str_object and r.start_datetime <=end_object) or (r.end_datetime <= end_object and r.end_datetime >= str_object) or (r.end_datetime >= end_object and r.start_datetime <= str_object) ).sorted(key=lambda r: r.start_datetime)


        # planns_ids = self.env['planning.slot'].search([('start_datetime','>=', str_object),('end_datetime','<=', end_object)]).filtered(lambda r: r.employee_id.user_id.id == self.env.uid)

        # return planns_ids

        for p in planns_ids:
            if p.task_id.stage_id.id == 63:
                lst1.append(p.task_id.id)
            elif p.task_id.stage_id.id == 71:
                lst2.append(p.task_id.id)
            elif p.task_id.stage_id.id == 65:
                lst3.append(p.task_id.id)

        dicta['En Cours'] = list(set(lst1))
        dicta['En Validation'] = list(set(lst2)) 
        dicta['TERMINE'] = list(set(lst3))  

        _logger.info("loadingggggggggggggggggggggggg %s/%s", str_object, end_object)
        task_ids = self.env['project.task'].search([('start_datetime', '>=', str_object), ('end_datetime', '<=', end_object),('planns', '!=', False)]).ids
        #("user_id" , "=", 163)
        #for task in task_ids :
        #    _logger.info("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM LLLL %s, %s, %s", task.id, task.start_datetime, task.end_datetime)
        #['&', ('start_datetime', '>=', str_object), ('end_datetime', '<=', end_object)]
        return dicta
#    in_active_week = fields.Boolean(string="In Active Week ?", compute='_compute_in_active_week', store=True,
#                                    default=False)

#    @api.depends('planns')
#    def _compute_in_active_week(self):
#        in_active_week = False

#        today = fields.datetime.today()
#        w_start = today - timedelta(days=today.weekday())
#        week_start = w_start.replace(microsecond=0, second=0, minute=0, hour=0)
#        w_end = week_start + timedelta(days=6)
#        week_end = w_end.replace(microsecond=999999, second=59, minute=59, hour=23)

#        self.in_active_week = False
#        if self.planns :
#            for rec in self.planns:
#                if rec.end_datetime and rec.end_datetime >= week_start and rec.end_datetime <= week_end:
#                    in_active_week = True
#        self.in_active_week = in_active_week


#    in_next_week = fields.Boolean(string="In Active Week ?", compute='_compute_in_next_week', store=True,
#                                    default=False)
#    @api.depends('planns')
#    def _compute_in_next_week(self):
#        in_next_week = False

#        today = fields.datetime.today()
#        n_w_start = today - timedelta(days=today.weekday()-7)
#        n_week_start = n_w_start.replace(microsecond=0, second=0, minute=0, hour=0)
#        n_w_end = n_week_start + timedelta(days=6)
#        n_week_end = n_w_end.replace(microsecond=999999, second=59, minute=59, hour=23)

#        self.in_next_week = False
#        if self.planns :
#            for rec in self.planns:
#                if rec.end_datetime and rec.end_datetime >= n_week_start and rec.end_datetime <= n_week_end:
#                    in_next_week = True
#        self.in_next_week = in_next_week

