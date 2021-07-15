# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning





class DecimalPprecision(models.Model):
    _inherit = 'project.task'



    planns = fields.Many2many('planning.slot', 'palann_id2', string="Planning")

    def action_add_plann(self):

        view_id = self.env.ref('planning.planning_view_form').id

        # context = {'project_id':self.project_id,'task_id':self.id}
        context = dict()

        context.update({

            'default_project_id':self.project_id.id,

            'default_task_id':self.id,
            'default_employee_id':self.user_id.employee_id.id,

        })

        return {

                'name':'Planning',

                'view_mode': 'form',

                # 'view_mode':'tree',

                'views' : [(view_id,'form')],

                'res_model':'planning.slot',

                'view_id':view_id,

                'type':'ir.actions.act_window',

                # 'res_id':self.id,

                'target':'new',

                'context':context,

                }


class Planningoverr(models.Model):
    _inherit = 'planning.slot'


    @api.model
    def create(self, values):
        res = super(Planningoverr, self).create(values)
        if res.task_id: 
          data = self.env['project.task'].search([('id','=',res.task_id.id)])
          data.planns = [(4, res.id)]
        return res

    # def unlink(self):

    #     for m in self:
    #         data = self.env['project.task'].search([('id','=', m.task_id.id)])
    #         data.planns = [(2, m.id)]
        
    #     return super(Planningoverr,self).unlink()
       