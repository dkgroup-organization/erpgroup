# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime

class delier_project_cancel_sale(models.Model):
    _inherit = "sale.order"

    def action_cancel(self):
        for r in self:
            r.projet.devis = [(3, r.id)]
            r.projet = False
        super(delier_project_cancel_sale, self).action_cancel()


class delier_project_cancel_purchase(models.Model):
    _inherit = "purchase.order"

    def button_cancel(self):
        for r in self:
            r.projet.achats = [(3, r.id)]
            r.projet = False
        super(delier_project_cancel_purchase, self).button_cancel()

class delier_project_cancel_move(models.Model):
    _inherit = "account.move"

    def button_cancel(self):
        for r in self:
            r.projet.factures = [(3, r.id)]
            r.projet.factures_fournisseurs = [(3, r.id)]
            r.projet = False
        super(delier_project_cancel_move, self).button_cancel()
