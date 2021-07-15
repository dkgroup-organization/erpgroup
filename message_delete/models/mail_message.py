# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import UserError


class mail_message(models.Model):
    """
    Overwrite to make sure unlink is done by ERP managers
    """
    _name = 'mail.message'
    _inherit = 'mail.message'

    def unlink(self):
        """
        Overwrite to add the extra security check
        """
        if self._context.get('message_delete'):
            if not self.env.user.has_group("sales_team.group_sale_manager"):
                raise UserError((_('Only Odoo administrators can delete messages.')))
        return super(mail_message, self).unlink()
