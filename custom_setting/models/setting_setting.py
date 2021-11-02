# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging
_logger = logging.getLogger(__name__)

class setting_setting_aydoo(models.TransientModel):
    _name = 'setting.setting'
    _description = 'Setting'

    def update_moves_amount(self):
        moves = self.env['account.move'].search([('type','in',('out_invoice','in_invoice')),('state','in',('draft','cancel'))])
        _logger.info("nbre de factures %s" % (len(moves)))
        i=0
        for p in moves:
            i+=1
            _logger.info("Eteration %s" % (i))
            _logger.info("N° factures est  %s est %s" % (p.name,p.id))
            p._compute_amount()

    def get_moves_list(self):
        moves = self.env['account.move'].search([('amount_residual','=',0),('type','=','out_invoice'),('state','=',"posted"),('invoice_payments_widget','=',False)])
        move=moves[0]
        raise UserError(" payment_state %s json %s et type %s" %(move.payment_state,move.invoice_payments_widget,type(move.invoice_payments_widget)))
        raise UserError(len(moves))



