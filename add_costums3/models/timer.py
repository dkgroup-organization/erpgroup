from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import groupby
from odoo.exceptions import Warning
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_round
from datetime import datetime

from distutils.util import strtobool 
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re




class AccountMove23(models.Model):
    _inherit = "account.move"
    def action_invoice_sent(self):
       """ Open a window to compose an email, with the edi invoice template
        message loaded by default
       """
       if self.partner_id.street and self.partner_id.city and self.partner_id.zip and self.x_contact:
        self.ensure_one()
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        lang = get_lang(self.env)
        if template and template.lang:
            lang = template._render_template(template.lang, 'account.move', self.id)
        else:
            lang = lang.code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)


        templ = self.env['mail.template'].search([('name', 'ilike', self.company_id.name),('model_id','=','account.move')])
        if templ:
           ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            default_partner_ids=[(4, self.x_contact.id)],
            default_use_template=bool(template),
            default_template_id=templ.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        else:

            ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            default_partner_ids=[(4, self.x_contact.id)],
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
       else:
           raise UserError(_('Verifier l\'adresse et le contact du client'))







class SaleOrderLine2(models.Model):
    _inherit = 'sale.order.line'
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        # if self.order_id.pricelist_id and self.order_id.partner_id:
        #     product = self.product_id.with_context(
        #         lang=self.order_id.partner_id.lang,
        #         partner=self.order_id.partner_id,
        #         quantity=self.product_uom_qty,
        #         date=self.order_id.date_order,
        #         pricelist=self.order_id.pricelist_id.id,
        #         uom=self.product_uom.id,
        #         fiscal_position=self.env.context.get('fiscal_position')
        #     )
        #     self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        
        
        
class saleoderd(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        # ensure a correct context for the _get_default_journal method and company-dependent fields
        self = self.with_context(default_company_id=self.company_id.id, force_company=self.company_id.id)
        journal = self.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'invoice_user_id': self.user_id and self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'invoice_partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_payment_ref': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'x_sale_id': self.id,
            'x_contact': self.x_contact.id,
            'x_objet': self.x_objet,
            'required_numero_commande':self.required_numero_commande,
            'numero_commande':self.numero_commande,
            'ref_client': self.ref_client,
            'x_reference': self.x_reference,
            'piece_joint': [(6, 0, self.piece_joint.ids)],
            'achats': [(6, 0, self.vents_lies.ids)],
        }
        return invoice_vals

