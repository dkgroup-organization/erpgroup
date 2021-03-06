from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

import logging

_logger = logging.getLogger(__name__)

from werkzeug.urls import url_encode


class facture(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id')
    def _onchange_partner_id_add_adress(self):
        if self.partner_id:
            if self.partner_id.child_ids:
                child_ids = self.partner_id.child_ids
                if child_ids:
                    item_ids = [line_ for line_ in child_ids if line_.type == "invoice"]
                    if item_ids:
                        variable_ = item_ids[0].id
                        if variable_:
                            self.x_contact = variable_


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

        # def create_invoices(self):
        #     sale_order = self.env['sale.order']
        #     sale_order._create_invoices()
        #
        #     return super(PaymentInv, self).create_invoices()


class account(models.Model):
    _inherit = 'sale.order'


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




