# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class task_task_limite(models.Model):
    _inherit = 'project.task'

    date_deadline = fields.Datetime(string='Deadline', index=True, copy=False, tracking=True)
    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")

class task_task_ticket_button(models.Model):
    _inherit = 'planning.slot'

    def open_task(self):
     if self.task_id:
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://dkgroup.odoo.com/web#cids=36&id=%s&model=project.task' % (self.task_id.id),
            'target': 'new',
        }
    
    def open_ticket(self):
     if self.task_id.ticket_id:
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://erp.dkgroup.fr/web#cids=36&id=%s&model=helpdesk.ticket&menu_id=' % (self.task_id.ticket_id.id),
            'target': 'new',
        }
