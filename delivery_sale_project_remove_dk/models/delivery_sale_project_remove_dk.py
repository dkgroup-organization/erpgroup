from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class delivery_sale_project_remove_dk_inherited(models.Model):
    _inherit = 'purchase.order'

    # achat_test = fields.Many2one('purchase.order', string='Achats', required=True)

    # @api.onchange('achat')
    # def _getfilter(self):
    #     data = self.env['project.project'].browse(self._context.get('active_ids', []))
    #     return {'domain': {'achat': [('id', 'in', data.achats.ids)]}}

    def action_delier_achat(self):
        data = self.env['purchase.order'].search([("id", "=", self.id)])
        self.projet = False
        data = [(3, self.id)]

class delivery_facture_project_remove_dk_inherited(models.Model):
    _inherit = 'account.move'

    def action_delier_account(self):
        data = self.env['account.move'].search([("id", "=", self.id)])
        self.projet = False
        data = [(3, self.id)]

class delivery_vende_project_remove_dk_inherited(models.Model):
    _inherit = 'sale.order'

    def action_delier_sale(self):
        data = self.env['sale.order'].search([("id", "=", self.id)])
        self.projet = False
        data = [(3, self.id)]









