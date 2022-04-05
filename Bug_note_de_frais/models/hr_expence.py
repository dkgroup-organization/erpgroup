from odoo import api, fields, models, _
from odoo.exceptions import ValidationError,UserError

import logging


_logger = logging.getLogger( __name__ )


class hr_expense(models.Model):
    _inherit = 'hr.expense'



    def new_button(self):
        test = self._create_sheet_from_expenses()
        test.action_submit_sheet()
        _logger.info('fffffffffffffffffffff %s',test)
        return {
            'name': _('New Expense Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense.sheet',
            'target': 'current',
            'res_id': test.id,
        }



