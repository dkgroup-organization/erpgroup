odoo.define('payment_stripe_checkout.stripe_checkout', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');

    var _t = core._t;

    if ($.blockUI) {
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }

    var StripeCheckoutRedirect = Widget.extend({
        init: function() {
            this.stripe_checkout = undefined;
            this.form = $('form[provider="stripe_checkout"]');
            this._initBlockUI(_t("Loading Stripe JS..."));
            this.willStart();
        },
        willStart: function () {
            var self = this;
            return ajax.loadJS("https://js.stripe.com/v3/").then(function() {
                self._initBlockUI(_t("Creating Checkout Session..."));
                self.start();
            })
        },
        start: function () {
            var publishable_key = $("input[name='stripe_checkout_pub_key']").first().val();
            this.stripe_checkout = Stripe(publishable_key);
            this._createCheckoutSession();
        },
        _createCheckoutSession: function() {
            var self = this;
            ajax.jsonRpc('/payment/stripe_checkout/create_checkout_session', 'call', self._getFormData())
            .then(function (result) {
                if (result.status) {
                    self._initBlockUI(_t("Redirecting to Stripe Checkout Page..."));
                    self._redirectStripeCheckout(result);
                } else {
                    self._showErrorMessage(_t("Stripe Error !!!"), result.message);
                }
            });
        },
        _redirectStripeCheckout: function(data) {
            var self = this;
            this.stripe_checkout.redirectToCheckout({
                sessionId: data.session_id
            }).then(function (result) {
                if (result.error) {
                    self._showErrorMessage(_t("Stripe Error !!!"), result.error.message);
                }
            });
        },
        _showErrorMessage: function(title, message) {
            this._revokeBlockUI();
            return new Dialog(null, {
                title: _t('Error: ') + _.str.escapeHTML(title),
                size: 'medium',
                $content: "<p>" + (_.str.escapeHTML(message) || "") + "</p>" ,
                buttons: [
                {text: _t('Ok'), close: true}]}).open();
        },
        _getFormData: function() {
            var data = {}
            this.form.find('input').each(function() {
                data[$(this).attr('name')] = $(this).val();
            });
            return data
        },
        _initBlockUI: function(message) {
            if ($.blockUI) {
                $.blockUI({
                    'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                            '    <br />' + message +
                            '</h2>'
                });
            }
            $("#o_payment_form_pay").attr('disabled', 'disabled');
        },
        _revokeBlockUI: function() {
            if ($.blockUI) {
                $.unblockUI();
            }
            $("#o_payment_form_pay").removeAttr('disabled');
        },
    });
    new StripeCheckoutRedirect();

});
