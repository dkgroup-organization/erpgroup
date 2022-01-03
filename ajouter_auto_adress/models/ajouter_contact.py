


from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

import logging

_logger = logging.getLogger(__name__)



from werkzeug.urls import url_encode


class facture(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, values):
        value["x_contact"] = self.env["res.partner"].search([('id', '=', 45291)]).id
        return super(facture, self).create(values)

    @api.onchange('partner_id')
    def _onchange_FIELD_NAME(self):
        self.x_contact = self.env["res.partner"].search([('id', '=', 45291)]).id
        for var in self:
            var.x_contact = var.env["res.partner"].search([('id', '=', 45291)])
            if var.partner_id:

                child_ids = var.partner_id.child_ids
                
                item_ids = [line_ for line_ in child_ids if line_.type == "invoice"]
             
                
             

class account(models.Model):
    _inherit = 'sale.order'

    # def _create_invoices(self, grouped=False, final=False, start_date=None, end_date=None):
    #     sale_order = self.env['sale.order']
    #     invoice_vals = sale_order._prepare_invoice()
    # 
    #     return super(account, self)._create_invoices(grouped, final)

    def _prepare_invoice(self):
        invoice_vals = super(account, self)._prepare_invoice()
        invoice_vals['x_contact'] = self.partner_invoice_id.id
        return invoice_vals
    # 
    # def _prepare_invoice(self):
    #     """
    #     Prepare the dict of values to create the new invoice for a sales order. This method may be
    #     overridden to implement custom invoice generation (making sure to call super() to establish
    #     a clean extension chain).
    #     """
    #     self.ensure_one()
    #     journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
    #     if not journal:
    #         raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (
    #             self.company_id.name, self.company_id.id))
    # 
    #     invoice_vals = {
    #         'ref': self.client_order_ref or '',
    #         'x_contact': self.partner_invoice_id.id,
    # 
    #         'move_type': 'out_invoice',
    #         'narration': self.note,
    #         'currency_id': self.pricelist_id.currency_id.id,
    #         'campaign_id': self.campaign_id.id,
    #         'medium_id': self.medium_id.id,
    #         'source_id': self.source_id.id,
    #         'user_id': self.user_id.id,
    #         'invoice_user_id': self.user_id.id,
    #         'team_id': self.team_id.id,
    #         'partner_id': self.partner_invoice_id.id,
    #         'partner_shipping_id': self.partner_shipping_id.id,
    #         'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(
    #             self.partner_invoice_id.id)).id,
    #         'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
    #         'journal_id': journal.id,  # company comes from the journal
    #         'invoice_origin': self.name,
    #         'invoice_payment_term_id': self.payment_term_id.id,
    #         'payment_reference': self.reference,
    #         'transaction_ids': [(6, 0, self.transaction_ids.ids)],
    #         'invoice_line_ids': [],
    #         'company_id': self.company_id.id,
    #     }
    #     return invoice_vals


class PaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # def create_invoices(self):
    #     sale_order = self.env['sale.order']
    #     sale_order._create_invoices()
    # 
    #     return super(PaymentInv, self).create_invoices()

