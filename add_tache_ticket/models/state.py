# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime
from datetime import timedelta, datetime
from odoo.exceptions import AccessError, UserError, ValidationError

class HelpdeskTicketaddtask(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        if self.task_id:
            if self.stage_id.id == 3:
                self.task_id.stage_id = 65

    def add_task(self):
      task = self.env['project.task']
      if self.project_id and self.user_id and self.name:
        c_task = task.create(
           {'project_id': self.project_id.id,
           'name': "Ticket - "+self.name,
           'user_id':self.user_id.id,
           'description':self.description,
           'ticket_id':self.id,
            
            })
        self.task_id = c_task.id
        
        current_date = fields.datetime.today()
        
        if self.priority == "3":
          date_test = current_date + timedelta(days=1)
          c_task.date_deadline = current_date + timedelta(days=1)
        
          data = {
          'res_id': c_task.id,
          'res_model_id': self.env['ir.model'].search([('model', '=', 'project.task')]).id,
          'user_id': self.user_id.id,
          'summary': 'Tâche à Faire sous 24 heures ',
          'activity_type_id': 4,
          'date_deadline': date_test
          }
          self.env['mail.activity'].create(data)
        if self.priority == "2":
          date_test = current_date + timedelta(days=2)
          c_task.date_deadline = current_date + timedelta(days=2)
        
          data = {
          'res_id': c_task.id,
          'res_model_id': self.env['ir.model'].search([('model', '=', 'project.task')]).id,
          'user_id': self.user_id.id,
          'summary': 'Tâche à Faire sous 48 heures ',
          'activity_type_id': 4,
          'date_deadline': date_test
          }
          self.env['mail.activity'].create(data)
        
        if self.priority == "1":
          date_test = current_date + timedelta(days=3)
          c_task.date_deadline = current_date + timedelta(days=3)
        
          data = {
          'res_id': c_task.id,
          'res_model_id': self.env['ir.model'].search([('model', '=', 'project.task')]).id,
          'user_id': self.user_id.id,
          'summary': 'Tâche à Faire 72 heures ',
          'activity_type_id': 4,
          'date_deadline': date_test
          }
          self.env['mail.activity'].create(data)
        
        if self.priority == "0":
          date_test = current_date + timedelta(days=7)
          c_task.date_deadline = current_date + timedelta(days=7)
        
          data = {
          'res_id': c_task.id,
          'res_model_id': self.env['ir.model'].search([('model', '=', 'project.task')]).id,
          'user_id': self.user_id.id,
          'summary': 'Tâche à Faire sous 6 jours',
          'activity_type_id': 4,
          'date_deadline': date_test
          }
          self.env['mail.activity'].create(data)
      else:
         raise UserError('Verifier les champs : Titre, Projet, Assigné à ...')

