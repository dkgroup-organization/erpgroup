odoo.define('payment_stripe_checkout.stripe_js', function (require) {
    "use strict";
    
    var ajax = require('web.ajax');
    var core = require('web.core');
    var PaymentForm = require('payment.payment_form');

    var _t = core._t;
    
    PaymentForm.include({
        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.options = _.extend(options || {}, {
            });
            this.stripe_checkout = undefined;
            this.stripe_checkout_card = undefined;
        },
        willStart: function () {
            return this._super.apply(this, arguments).then(function () {
                return ajax.loadJS("https://js.stripe.com/v3/");
            });
        },
        updateNewPaymentDisplayStatus: function () {
            var $checkedRadio = this.$('input[type="radio"]:checked');
            if ($checkedRadio.length !== 1) {
                return;
            }
            var provider = $checkedRadio.data('provider')
            if (provider === 'stripe_checkout') {
                this._unbindStripeCheckoutCard();
                if (this.isNewPaymentRadio($checkedRadio)) {
                    this._bindStripeCheckoutCard($checkedRadio);
                }
            }
            return this._super.apply(this, arguments);
        },
        _bindStripeCheckoutCard: function ($checkedRadio) {
            var acquirerID = this.getAcquirerIdFromRadio($checkedRadio);
            var acquirerForm = this.$('#o_payment_add_token_acq_' + acquirerID);
            var inputsForm = $('input', acquirerForm);
            var formData = this.getFormData(inputsForm);
            var stripe = Stripe(formData.stripe_checkout_pub_key);
            var element = stripe.elements();
            var style = {
                base: {
                  color: '#32325d',
                  fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                  fontSmoothing: 'antialiased',
                  fontSize: '16px',
                  '::placeholder': {
                    color: '#aab7c4'
                  }
                },
                invalid: {
                  color: '#fa755a',
                  iconColor: '#fa755a'
                }
            };
            var card = element.create('card', {hidePostalCode: true, style: style});
            card.mount('#stripe-checkout-card-element');
            card.on('ready', function(ev) {
                card.focus();
            });
            card.addEventListener('change', function (event) {
                var displayError = document.getElementById('stripe-checkout-card-errors');
                displayError.textContent = '';
                if (event.error) {
                    displayError.textContent = event.error.message;
                }
            });
            this.stripe_checkout = stripe;
            this.stripe_checkout_card = card;
        },
        _unbindStripeCheckoutCard: function () {
            if (this.stripe_checkout_card) {
                this.stripe_checkout_card.destroy();
            }
            this.stripe = undefined;
            this.stripe_checkout_card = undefined;
        },
        payEvent: function (ev) {
            ev.preventDefault();
            var $checkedRadio = this.$('input[type="radio"]:checked');
            
            if ($checkedRadio.data('is_stripe_checkout') === 'True' || ($checkedRadio.length === 1 && this.isNewPaymentRadio($checkedRadio) && $checkedRadio.data('provider') === 'stripe_checkout')) {
                return this._createStripePayment(ev, $checkedRadio);
            } else {
                return this._super.apply(this, arguments);
            }
        },
        addPmEvent: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var $checkedRadio = this.$('input[type="radio"]:checked');

            if ($checkedRadio.length === 1 && this.isNewPaymentRadio($checkedRadio) && $checkedRadio.data('provider') === 'stripe_checkout') {
                return this._createStripeToken(ev, $checkedRadio);
            } else {
                return this._super.apply(this, arguments);
            }
        },
        _createStripePayment: function(ev, $checkedRadio) {
            var self = this;
            if (ev.type === 'submit') {
                var button = $(ev.target).find('*[type="submit"]')[0]
            } else {
                var button = ev.target;
            }
            $(button).attr('disabled', true);
            $(button).children('.fa-plus-circle').removeClass('fa-plus-circle')
            $(button).prepend('<span class="o_loader"><i class="fa fa-refresh fa-spin"></i>&nbsp;</span>');

            var acquirerID = this.getAcquirerIdFromRadio($checkedRadio);
            var acquirerForm = this.$('#o_payment_add_token_acq_' + acquirerID);
            var inputsForm = $('input', acquirerForm);
            var formData = this.getFormData(inputsForm);

            var tx_url = this.$el.find('input[name="prepare_tx_url"]').val();
            var order_id = tx_url.match(/my\/orders\/([0-9]+)/) || undefined;
            if (order_id) {
                _.extend(formData, {
                    'order_id': parseInt(order_id[1]),
                });
            }
            var invoice_id = tx_url.match(/invoice\/pay\/([0-9]+)/) || undefined;
            if (invoice_id) {
                _.extend(formData, {
                    'invoice_id': parseInt(invoice_id[1]),
                    'access_token': self.options.accessToken,
                    'success_url': self.options.successUrl,
                    'error_url': self.options.errorUrl,
                });
            } 
            if ($checkedRadio.data('is_stripe_checkout') === 'True') {
                _.extend(formData, {
                    "token": $checkedRadio.val(),
                    "acquirer_id": $checkedRadio.data('stripe_checkout_id'),
                    "return_url": "/shop/payment/validate",
                });
                return self._initDoPayment(formData, button);
            } else {
                var stripe = this.stripe_checkout;
                var card = this.stripe_checkout_card;
                if (card && card._invalid) {
                    return;
                }
                return stripe.createPaymentMethod('card', card, {
                    billing_details: {
                        name: formData.partner_name,
                        email: formData.partner_email
                    },
                }).then(function(result) {
                    if (result.error) {
                        self.displayError(_t("Stripe Error !!!"), result.error.message);
                        return Promise.reject({"message": {"data": { "message": result.error.message}}});
                    } else {
                        _.extend(formData, {"payment_method": result.paymentMethod.id});
                        self._initDoPayment(formData, button);
                    }
                });
            }
        },
        _initDoPayment: function(data, button) {
            var self = this;
            var stripe = this.stripe_checkout;
            return ajax.jsonRpc('/payment/stripe_checkout/do_payment', 'call', data)
            .then(function(result) {
                if (result.status) {
                    if (result.next_action) {
                        if (!stripe) {
                            // in case direct choose save stripe token
                            stripe = Stripe(result.stripe_checkout_pub_key);
                        }
                        return stripe.handleCardPayment(result.client_secret).then(function(resp) {
                            if (resp.error) {
                                self.displayError(_t("Stripe Error !!!"), resp.error.message);
                                return Promise.reject({"message": {"data": { "message": resp.error.message}}});
                            } else {
                                window.location = result.return_url;
                            }
                        });
                    } else {
                        window.location = result.return_url;
                    }
                } else {
                    if (result.return_url) {
                        window.location = result.return_url;
                    }
                    $(button).attr('disabled', false);
                    $(button).children('.fa').addClass('fa-plus-circle')
                    $(button).find('span.o_loader').remove();
                    self.displayError(_t("Stripe Error !!!"), result.message);
                }
            }).fail(function(result) {
                self.displayError(_t("Stripe Error !!!"), _t("Payment Failed, Some error occured while payment."));
            });
        },
        _createStripeToken: function(ev, $checkedRadio) {
            var self = this;
            if (ev.type === 'submit') {
                var button = $(ev.target).find('*[type="submit"]')[0]
            } else {
                var button = ev.target;
            }
            $(button).attr('disabled', true);
            $(button).children('.fa-plus-circle').removeClass('fa-plus-circle')
            $(button).prepend('<span class="o_loader"><i class="fa fa-refresh fa-spin"></i>&nbsp;</span>');

            var acquirerID = this.getAcquirerIdFromRadio($checkedRadio);
            var acquirerForm = this.$('#o_payment_add_token_acq_' + acquirerID);
            var inputsForm = $('input', acquirerForm);
            var formData = this.getFormData(inputsForm);
            var stripe = this.stripe_checkout;
            var card = this.stripe_checkout_card;
            if (card && card._invalid) {
                return;
            }
            ajax.jsonRpc('/payment/stripe_checkout/create_setup_intent', 'call', formData)
            .then(function (resp) {
                if (resp.status) {
                return stripe.handleCardSetup(resp.client_secret, card).then(function(result) {
                        if (result.error) {
                            self.displayError(_t("Stripe Error !!!"), result.error.message);
                            return Promise.reject({"message": {"data": { "message": result.error.message}}});
                        } else {
                            _.extend(formData, {"payment_method": result.setupIntent.payment_method});
                            return ajax.jsonRpc('/payment/stripe_checkout/s2s/save_card', 'call', formData)
                            .then(function(result) {
                                if (result.status) {
                                    window.location = formData.return_url;
                                } else {
                                    self.displayError(_t("Stripe Error !!!"), result.message);
                                }
                            }).fail(function(result) {
                                self.displayError(_t("Stripe Error !!!"), _t("Some error occured while saving your card data."));
                            });
                        }
                    });
                } else {
                    self.displayError(_t("Stripe Error !!!"), resp.message);
                }
            }).fail(function(result) {
                self.displayError(_t("Stripe Error !!!"), _t("Some error occured while saving your card data."));
            });
        },
        displayError: function (title, message) {
            var $checkedRadio = this.$('input[type="radio"]:checked'),
                acquirerID = this.getAcquirerIdFromRadio($checkedRadio[0]);
            var $acquirerForm;
            if (this.isNewPaymentRadio($checkedRadio[0])) {
                $acquirerForm = this.$('#o_payment_add_token_acq_' + acquirerID);
            }
            else if (this.isFormPaymentRadio($checkedRadio[0])) {
                $acquirerForm = this.$('#o_payment_form_acq_' + acquirerID);
            } else {
                $acquirerForm = $checkedRadio.parent('label');
            }

            if ($checkedRadio.length === 0) {
                return new Dialog(null, {
                    title: _t('Error: ') + _.str.escapeHTML(title),
                    size: 'medium',
                    $content: "<p>" + (_.str.escapeHTML(message) || "") + "</p>" ,
                    buttons: [
                    {text: _t('Ok'), close: true}]}).open();
            } else {
                // removed if exist error message
                this.$('#payment_error').remove();
                var messageResult = '<div class="alert alert-danger mb4" id="payment_error">';
                if (title != '') {
                    messageResult = messageResult + '<b>' + _.str.escapeHTML(title) + ':</b></br>';
                }
                messageResult = messageResult + _.str.escapeHTML(message) + '</div>';
                $acquirerForm.append(messageResult);
            }
        },
    });
});