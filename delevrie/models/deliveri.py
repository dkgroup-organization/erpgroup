from odoo import api, fields, models, _

class projectt(models.Model):
    _inherit = 'purchase.order'




    #achat_test = fields.Many2one('purchase.order', string='Achats', required=True)

    # @api.onchange('achat')
    # def _getfilter(self):
    #     data = self.env['project.project'].browse(self._context.get('active_ids', []))
    #     return {'domain': {'achat': [('id', 'in', data.achats.ids)]}}

    def action_delier_achat_t(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        for m in data:
            self.projet = False
            m = [(3, self.id)]





