# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging , json
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
        moves = self.env['account.move'].search([('amount_residual','=',0),('invoice_payment_state','=','paid'),('type','=','out_invoice'),('state','=',"posted")])
        moves_filtred = moves.filtered(lambda r: not json.loads(r.invoice_payments_widget))
        for move in moves_filtred:
            _logger.info("json %s et type %s et date de creation %s" %(move.invoice_payments_widget,type(move.invoice_payments_widget),move.create_date))
        raise UserError(" moves : %s ; filtered : %s "% (len(moves),len(moves_filtred)))

        raise UserError("json %s et type %s" %(move.invoice_payments_widget,type(move.invoice_payments_widget)))
        raise UserError(len(moves))



