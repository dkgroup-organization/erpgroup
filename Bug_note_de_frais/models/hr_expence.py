from odoo import api, fields, models, _
from odoo.exceptions import ValidationError,UserError

import logging


_logger = logging.getLogger( __name__ )


class hr_expense(models.Model):
    _inherit = 'hr.expense'



    def action_submit_sheet2(self):

        sheet = self._create_sheet_from_expenses()
        sheet.action_submit_sheet()
        _logger.info('fffffffffffffffffffff %s',sheet)
        return {
            'name': _('New Expense Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense.sheet',
            'target': 'current',
            'res_id': sheet.id,
        }



