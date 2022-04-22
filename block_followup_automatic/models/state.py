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

#     def _compute_for_followup(self):
#         """
#         Compute the fields 'total_due', 'total_overdue','followup_level' and 'followup_status'
#         """
#         first_followup_level = self.env['account_followup.followup.line'].search([('company_id', '=', self.env.company.id)], order="delay asc", limit=1)
#         followup_data = self._query_followup_level()
#         today = fields.Date.context_today(self)
#         for record in self:
#           if record.is_blocked == False:
#             total_due = 0
#             total_overdue = 0
#             for aml in record.unreconciled_aml_ids:
#                 if aml.company_id == self.env.company and not aml.blocked:
#                     amount = aml.amount_residual
#                     total_due += amount
#                     is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
#                     if is_overdue:
#                         total_overdue += amount
#             record.total_due = total_due
#             record.total_overdue = total_overdue
#             if record.id in followup_data:
#                 record.followup_status = followup_data[record.id]['followup_status']
#                 record.followup_level = self.env['account_followup.followup.line'].browse(followup_data[record.id]['followup_level']) or first_followup_level
#             else:
#                 record.followup_status = 'no_action_needed'
#                 record.followup_level = first_followup_level
#           else:
#             total_due = 0
#             total_overdue = 0
#             for aml in record.unreconciled_aml_ids:
#                 if aml.company_id == self.env.company and not aml.blocked:
#                     amount = aml.amount_residual
#                     total_due += amount
#                     is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
#                     if is_overdue:
#                         total_overdue += amount
#             record.total_due = total_due
#             record.total_overdue = total_overdue
#             if record.id in followup_data:
#                 record.followup_status = 'no_action_needed'
#                 record.followup_level = self.env['account_followup.followup.line'].browse(followup_data[record.id]['followup_level']) or first_followup_level
#             else:
#                 record.followup_status = 'no_action_needed'
#                 record.followup_level = first_followup_level
