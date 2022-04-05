from odoo import api, fields, models, _
from odoo.exceptions import ValidationError,UserError

import logging


_logger = logging.getLogger( __name__ )


class hr_expense(models.Model):
    _inherit = 'hr.expense'



    def new_button(self):
        test = self._create_sheet_from_expenses()
        _logger.info('fffffffffffffffffffff %s',test)



