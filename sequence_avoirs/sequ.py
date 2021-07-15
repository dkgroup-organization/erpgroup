# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class SequAvr(models.Model):
    _inherit = 'account.invoice'

    # @api.model
    # def create(self, vals):
    #   res = super(SequAvr, self).create(vals)
    #   if res.type == 'out_refund':
    #      res.number = self.env['ir.sequence'].next_by_code('sequ_avr') or _('New')
    #   return res


    # def action_invoice_open(self):
    #   for m in self:
    #     if self.type == 'out_refund':
    #        self.number = self.env['ir.sequence'].next_by_code('sequ_avr') or _('New')
    #   rs = super(SequAvr, self).action_invoice_open()
    #   return rs

    # def action_move_create(self):
    #   for m in self:
    #     if m.type == 'out_refund':
    #        m.number = self.env['ir.sequence'].next_by_code('sequ_avr') or _('New')
    #   r = super(SequAvr, self).action_move_create()
    #   return r

    def invoice_validate(self):
      for m in self:
        if m.type == 'out_refund':
           m.number = self.env['ir.sequence'].next_by_code('sequ_avr') or _('New')
      rse = super(SequAvr, self).invoice_validate()
      return rse