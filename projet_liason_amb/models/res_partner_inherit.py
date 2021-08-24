from odoo import api, exceptions, fields, models, _

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    is_manager = fields.Boolean('Administrateur',compute="_get_groups_access")
    project_manager = fields.Many2one('res.partner')
    technical_controller = fields.Many2one('res.partner')

    def _get_groups_access(self):
        for record in self:
            record.is_manager = self.env.user.has_group('account.group_account_manager')