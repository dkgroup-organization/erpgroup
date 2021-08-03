# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class acompte(models.Model):
    _inherit = 'project.project'

  
    amount_untaxed_achats = fields.Monetary(string='Total HT des achats', store=True, readonly=True, compute='_amount_all2', tracking=True)
    amount_total_achats = fields.Monetary(string='Total TTC des Achats', store=True, readonly=True, compute='_amount_all2')

    #@api.depends('achats')
    def _amount_all2(self):
        for project in self:
            amount_untaxed = amount_total = 0.0
            for line in project.achats:
                amount_untaxed += line.amount_untaxed
                amount_total += line.amount_total
            project.update({
                'amount_untaxed_achats': amount_untaxed,
                'amount_total_achats': amount_total,
                
            })


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_auto_subscribe(self, updated_fields,followers_existing_policy):
        super(MailThread, self)._message_auto_subscribe(updated_fields)
