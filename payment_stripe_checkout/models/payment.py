# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################
import logging
from werkzeug import urls
import pprint

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_round
from ..models.stripe_connector import StripeConnector
from odoo.addons.payment_stripe_checkout.controllers.main import StripeCheckoutController

_logger = logging.getLogger(__name__)
ZERO_DECIMAL_CURRENCIES = [
    'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYGí',
    'RWF', 'KRW', 'VUV', 'VND', 'XOF'
]


class AcquirerStripeCheckout(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('stripe_checkout', 'Stripe Checkout')])
    stripe_checkout_client_secret_key = fields.Char(string='Secret Key ', required_if_provider='stripe_checkout', groups='base.group_user')
    stripe_checkout_publishable_key = fields.Char(string='Publishable Key', required_if_provider='stripe_checkout', groups='base.group_user')

    @api.model
    def _create_missing_journal_for_acquirers(self, company=None):
        acquirers = self.env['payment.acquirer'].search([('provider', '=', 'stripe_checkout'), ('journal_id', '=', False)])
        journals = self.env['account.journal']
        for acquirer in acquirers.filtered(lambda l: not l.journal_id and l.company_id.chart_template_id):
            journal = journals.search([('name', '=', acquirer.name)])
            if journal:
                acquirer.journal_id = journal
            else:
                acquirer.journal_id = self.env['account.journal'].create(acquirer._prepare_account_journal_vals())
            journals += acquirer.journal_id
        return super(AcquirerStripeCheckout, self)._create_missing_journal_for_acquirers(company=company)

    def _stripe_call(self, method, operation='create', **params):
        self.ensure_one()
        StripeConn = StripeConnector(
            api_key=self.sudo().stripe_checkout_client_secret_key
        )
        if hasattr(StripeConn, method):
            return getattr(StripeConn, method)(operation, **params)
        return {
            'status': False,
            'message': _('Error: Please contact your service provider.'),
            'response': False
        }

    def _create_checkout_session(self, tx_data):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        partner = self.env['res.partner'].sudo().browse(int(tx_data.get('partner_id', 0)))
        customer_id = partner.stripe_checkout_create_customer(self.id)
        amount = float(tx_data['amount'])
        success_url = StripeCheckoutController._checkout_success_url
        cancel_url = StripeCheckoutController._checkout_cancel_url
        reference = tx_data['invoice_num']
        session_dict = {
            'payment_method_types[]': 'card',
            'line_items[][amount]': int(amount if str(tx_data['currency_name']) in ZERO_DECIMAL_CURRENCIES else float_round(amount * 100, 2)),
            'line_items[][currency]': tx_data['currency_name'],
            'line_items[][quantity]': 1,
            'line_items[][name]': reference,
            'client_reference_id': reference,
            'success_url': urls.url_join(base_url, success_url) + '?reference=%s' % reference,
            'cancel_url': urls.url_join(base_url, cancel_url) + '?reference=%s' % reference,
            'customer': customer_id,
            'payment_intent_data[description]': "Payment for %s: %s" % (partner.email, reference),
        }
        if self.capture_manually:
            session_dict['payment_intent_data[capture_method]'] = 'manual'

        res = self._stripe_call(
            method='_checkout_session',
            operation='create',
            **session_dict
        )
        if res['status'] and res['response'].get('payment_intent') and reference:
            tx = self.env['payment.transaction'].sudo().search([('reference', '=', reference)])
            tx.stripe_checkout_payment_intent = res['response']['payment_intent']
        return res

    def _create_setup_intent(self, kwargs):
        self.ensure_one()
        vals = {
            'usage': 'off_session',
            'payment_method_options[card][request_three_d_secure]': 'any'
        }
        res = self._stripe_call(
            method='_setup_intent',
            operation='create',
            **vals
        )
        return res

    @api.model
    def stripe_checkout_s2s_form_process(self, data):
        last4 = data.get('card', {}).get('last4')
        cc_name = data.get('cc_name')
        if not last4:
            res = self._stripe_call(
                    method='_payment_method',
                    operation='retrieve',
                    **{'id': data.get('payment_method')}
                )
            last4 = res['response'].get('card', {}).get('last4', '****')
            cc_name = res.get('billing_details', {}).get('name')

        if not cc_name:
            partner = self.env['res.partner'].sudo().browse(int(data['partner_id']))
            cc_name = partner.name

        payment_token = self.env['payment.token'].sudo().create({
            'acquirer_id': self.id,
            'partner_id': int(data['partner_id']),
            'stripe_checkout_payment_method': data.get('payment_method'),
            'name': 'XXXXXXXXXXXX%s - %s' % (last4, cc_name),
            'acquirer_ref': data.get('customer')
        })
        payment_token.verified = True
        return payment_token

    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(AcquirerStripeCheckout, self)._get_feature_support()
        res['authorize'].append('stripe_checkout')
        res['tokenize'].append('stripe_checkout')
        return res


class TransactionStripeCheckout(models.Model):
    _inherit = 'payment.transaction'

    stripe_checkout_payment_intent = fields.Char(string='Payment Intent ID', readonly=True)

    def create_payment(self, values):
        self.ensure_one()
        pm_id = self.payment_token_id
        if pm_id:
            values['payment_method'] = pm_id.stripe_checkout_payment_method

        if not values.get('payment_method'):
            return {
                'status': False,
                'message': _("Paymant Method not Found.")
            }

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        customer_id = self.partner_id.stripe_checkout_create_customer(self.acquirer_id.id)
        success_url = StripeCheckoutController._checkout_success_url
        return_url = urls.url_join(base_url, success_url) + '?reference=%s' % self.reference

        intent_params = {
            'amount': int(self.amount if str(self.currency_id.name) in ZERO_DECIMAL_CURRENCIES else float_round(self.amount * 100, 2)),
            'currency': self.currency_id.name,
            'setup_future_usage': 'off_session',
            'confirm': True,
            'payment_method': values['payment_method'],
            'customer': customer_id,
            'return_url': return_url,
            'payment_method_options[card][request_three_d_secure]': 'any',
            'description': "Payment for %s: %s" % (self.partner_id.email, self.reference),
        }
        if self.acquirer_id.capture_manually:
            intent_params['capture_method'] = 'manual'

        if not pm_id:
            res = self.acquirer_id._stripe_call(
                method='_payment_method',
                operation='attach',
                **{
                    'sid': values['payment_method'],
                    'customer': customer_id
                }
            )
            if not res['status']:
                return res

        _logger.info('create_payment: Sending values to stripe checkout, values:\n%s', pprint.pformat(intent_params))
        res = self.acquirer_id._stripe_call(
            method='_payment_intent',
            operation='create',
            **intent_params
        )

        if not res['status']:
            return res

        self.stripe_checkout_payment_intent = res['response'].get('id')
        return {
            'status': True,
            'next_action': res['response'].get('next_action', {}),
            'payment_intent': res['response'].get('id'),
            'client_secret': res['response'].get('client_secret'),
            'payment_method': res['response'].get('payment_method'),
            'return_url': return_url,
            'stripe_checkout_pub_key': self.acquirer_id.sudo().stripe_checkout_publishable_key
        }

    def refund_payment(self, amount=None):
        if not self.stripe_checkout_payment_intent:
            raise ValidationError(_('Only transactions having the acquirer reference can be refund.'))

        if not amount:
            amount = self.amount
        amount = int(amount if str(self.currency_id.name) in ZERO_DECIMAL_CURRENCIES else float_round(amount * 100, 2))
        res = self.acquirer_id._stripe_call(
            method='_refunds',
            operation='create',
            **{
                'charge': self.acquirer_reference,
                'amount': amount
            }
        )
        if not res['status']:
            raise ValidationError(res['message'])
        return res

    def capture_payment(self, amount=None):
        if not self.stripe_checkout_payment_intent:
            raise ValidationError(_('Only transactions having the payment intent can be captured.'))

        if not amount:
            amount = self.amount
        amount = int(amount if str(self.currency_id.name) in ZERO_DECIMAL_CURRENCIES else float_round(amount * 100, 2))
        res = self.acquirer_id._stripe_call(
            method='_payment_intent',
            operation='capture',
            **{
                'sid': self.stripe_checkout_payment_intent,
                'amount_to_capture': amount
            }
        )
        if not res['status']:
            raise ValidationError(res['message'])
        if res['status'] and res['response'].get('status') == 'succeeded':
            self._set_transaction_done()
        return res

    def cancel_payment(self):
        if not self.stripe_checkout_payment_intent:
            raise ValidationError(_('Only transactions having the payment intent can be cancel.'))

        res = self.acquirer_id._stripe_call(
            method='_payment_intent',
            operation='cancel',
            **{
                'sid': self.stripe_checkout_payment_intent
            }
        )
        if not res['status']:
            raise ValidationError(res['message'])
        if res['status'] and res['response'].get('status') == 'canceled':
            self._set_transaction_cancel()
        return res

    def stripe_checkout_s2s_capture_transaction(self, **kwargs):
        self.ensure_one()
        return self.capture_payment()

    def stripe_checkout_s2s_void_transaction(self, **kwargs):
        self.ensure_one()
        return self.cancel_payment()

    def stripe_checkout_s2s_do_refund(self, **kwargs):
        self.ensure_one()
        return self.refund_payment()

    @api.model
    def _stripe_checkout_form_get_tx_from_data(self, data):
        """ Given a data dict coming from stripe checkout, verify it and find the related
        transaction record. """
        reference = data.get('reference')
        if not reference:
            stripe_checkout_error = data.get('error', {}).get('message', '')
            _logger.error('Stripe Checkout: invalid reply received from stripe checkout API, looks like '
                          'the transaction failed. (error: %s)', stripe_checkout_error or 'n/a')
            error_msg = _("We're sorry to report that the transaction has failed.")
            if stripe_checkout_error:
                error_msg += " " + (_("Stripe checkout gave us the following info about the problem: '%s'") %
                                    stripe_checkout_error)
            error_msg += " " + _("Perhaps the problem can be solved by double-checking your "
                                 "credit card details, or contacting your bank?")
            raise ValidationError(error_msg)

        tx = self.search([('reference', '=', reference)])
        if not tx:
            error_msg = (_('Stripe Checkout: no order found for reference %s') % reference)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        elif len(tx) > 1:
            error_msg = (_('Stripe Checkout: %s orders found for reference %s') % (len(tx), reference))
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    def _stripe_checkout_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if data.get('amount') != int(self.amount if str(self.currency_id.name) in ZERO_DECIMAL_CURRENCIES else float_round(self.amount * 100, 2)):
            invalid_parameters.append(('Amount', data.get('amount'), self.amount * 100))
        if data.get('currency').upper() != self.currency_id.name:
            invalid_parameters.append(('Currency', data.get('currency'), self.currency_id.name))
        if data.get('payment_intent') and data.get('payment_intent') != self.stripe_checkout_payment_intent:
            invalid_parameters.append(('Payment Intent', data.get('payment_intent'), self.stripe_checkout_payment_intent))
        return invalid_parameters

    def _stripe_checkout_s2s_validate_tree(self, tree):
        self.ensure_one()
        if self.state != 'draft':
            _logger.info('Stripe Checkout: trying to validate an already validated tx (ref %s)', self.reference)
            return True

        status, tx_id, captured = tree.get('status'), tree.get('id'), tree.get('captured')
        vals = {
            'date': fields.datetime.now(),
            'acquirer_reference': tx_id,
        }
        if status == 'succeeded':
            self.write(vals)
            if captured:
                self._set_transaction_done()
            else:
                self._set_transaction_authorized()
            self.execute_callback()

            if not self.payment_token_id and self.type in ['form_save', 'server2server']:
                s2s_data = {
                    'customer': tree.get('customer'),
                    'payment_method': tree.get('payment_method'),
                    'card': tree.get('payment_method_details').get('card'),
                    'acquirer_id': self.acquirer_id.id,
                    'partner_id': self.partner_id.id,
                    'cc_name': tree.get('billing_details', {}).get('name'),
                }
                if not s2s_data['cc_name']:
                    s2s_data['cc_name'] = self.partner_id.name

                token = self.acquirer_id.stripe_checkout_s2s_form_process(s2s_data)
                self.payment_token_id = token.id

            if self.payment_token_id:
                self.payment_token_id.verified = True
            return True
        if status in ('processing', 'requires_action'):
            self.write(vals)
            self._set_transaction_pending()
            return True
        else:
            error = tree.get('failure_message')
            _logger.warn(error)
            vals.update({'state_message': error})
            self.write(vals)
            self._set_transaction_cancel()
            return False

    def _stripe_checkout_form_validate(self,  data):
        return self._stripe_checkout_s2s_validate_tree(data)


class TokenStripeCheckout(models.Model):
    _inherit = 'payment.token'

    stripe_checkout_payment_method = fields.Char('Payment Method ID')

    @api.model
    def stripe_checkout_create(self, values):
        if values.get('stripe_checkout_payment_method') and not values.get('acquirer_ref'):
            partner = self.env['res.partner'].browse(values.get('partner_id'))
            acquirer = self.env['payment.acquirer'].browse(values.get('acquirer_id'))

            customer_id = partner.stripe_checkout_create_customer(values.get('acquirer_id'))
            acquirer._stripe_call(
                method='_payment_method',
                operation='attach',
                **{
                    'sid': values['stripe_checkout_payment_method'],
                    'customer': customer_id
                }
            )

            return {
                'acquirer_ref': customer_id,
            }
        return values


class ResPartner(models.Model):
    _inherit = 'res.partner'

    stripe_checkout_customer_id = fields.Char('Stripe Customer ID')

    def stripe_checkout_create_customer(self, acquirer_id=None):
        self.ensure_one()
        acquirer = self.env['payment.acquirer'].browse(acquirer_id)
        customer_id = self.stripe_checkout_customer_id
        is_exist = True

        if customer_id:
            # check customer exist on stripe
            resp = acquirer._stripe_call(
                method='_customers',
                operation='retrieve',
                **{'id': customer_id}
            )
            if not resp['status'] and resp.get('response_code') == 404:
                is_exist = False

        if not (is_exist and customer_id) and acquirer_id:
            customer_data = {
                'email': self.email,
                'name': self.name,
            }
            cust_resp = acquirer._stripe_call(
                            method='_customers',
                            operation='create',
                            **customer_data
                        )
            if cust_resp['status']:
                customer_id = cust_resp['response'].get('id')
                self.stripe_checkout_customer_id = customer_id
        return customer_id
