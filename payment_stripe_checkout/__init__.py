# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################
from . import controllers
from . import models
from odoo.addons.payment.models.payment_acquirer import create_missing_journal_for_acquirers


def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import Warning
    version_info = common.exp_version()
    server_series = version_info.get('server_serie')
    if server_series != '12.0':
        raise Warning('Module support Odoo series 12.0 found {}'.format(server_series))
    return True


def setup_stripe_data(cr, registry):
    import stripe
    stripe.set_app_info(
        "ODOO Webkul Stripe Payment Acquirer",
        version=stripe.version.VERSION,
        url="https://webkul.com/",
        # partner_id='partner_12345'
    )
    create_missing_journal_for_acquirers(cr, registry)
