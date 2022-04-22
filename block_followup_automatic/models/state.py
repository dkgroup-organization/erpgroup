import logging
from odoo import api, fields, models, _
from odoo.tools.misc import format_date
from odoo.osv import expression
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_blocked = fields.Boolean(string='Bloquer les relances automatiques', default=False)

    def _cron_execute_followup_company(self):
        followup_data = self._query_followup_level(all_partners=True)
        in_need_of_action = self.env['res.partner'].browse([d['partner_id'] for d in followup_data.values() if d['followup_status'] == 'in_need_of_action' and d.is_blocked == False])
        in_need_of_action_auto = in_need_of_action.filtered(lambda p: p.followup_level.auto_execute)
        for partner in in_need_of_action_auto:
            try:
                partner._execute_followup_partner()
            except UserError as e:
                # followup may raise exception due to configuration issues
                # i.e. partner missing email
                _logger.exception(e)
