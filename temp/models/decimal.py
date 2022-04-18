# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
import logging
from odoo import api, fields, models, _
from odoo.tools.misc import format_date
from odoo.osv import expression
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

class DecimalPprecision(models.Model):
    _inherit = 'sale.order'

    vents_lies = fields.Many2many("purchase.order",'sale_order_move_rel',string="Ventes liés")
    somme = fields.Float(string="Total achats", compute='_count_somme',readonly=True)
    marge = fields.Float(string="Marge bénéficiaire", compute='_count_marge', readonly=True)
    recompute_delivery_price = fields.Boolean('Delivery cost should be recomputed')
   



class ResPartner2(models.Model):
    _inherit = 'res.partner'

    def update_next_action(self, options=False):
        """Updates the next_action_date of the right account move lines"""
        next_action_date = options.get('next_action_date') and options['next_action_date'][0:10] or False
        next_action_date_done = False
        today = date.today()
        fups = self._compute_followup_lines()
        for partner in self:
            if options['action'] == 'done':
                next_action_date_done = datetime.strftime(partner.followup_level._get_next_date(), DEFAULT_SERVER_DATE_FORMAT)
            partner.payment_next_action_date = (not next_action_date or options['action'] == 'done') and next_action_date_done or next_action_date
            if options['action'] in ('done', 'later'):
                msg = _('Next Reminder Date set to %s') % format_date(self.env, partner.payment_next_action_date)
                partner.message_post(body=msg)
            if options['action'] == 'done':
                for aml in partner.unreconciled_aml_ids:
                    index = None
                    followup_date = fups[index][0]
                    next_level = fups[index][1]
                    is_overdue = followup_date >= aml.date_maturity if aml.date_maturity else followup_date >= aml.date
                    if is_overdue:
                        aml.write({'followup_line_id': next_level, 'followup_date': today})
