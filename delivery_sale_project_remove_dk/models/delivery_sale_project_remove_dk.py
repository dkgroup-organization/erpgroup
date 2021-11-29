from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError



import logging,pprint

_logger = logging.getLogger(__name__)

class delivery_sale_project_remove_dk_inherited(models.Model):
    _inherit = 'purchase.order'




    #achat_test = fields.Many2one('purchase.order', string='Achats', required=True)

    # @api.onchange('achat')
    # def _getfilter(self):
    #     data = self.env['project.project'].browse(self._context.get('active_ids', []))
    #     return {'domain': {'achat': [('id', 'in', data.achats.ids)]}}

    def action_delier_achat(self):
        data = self.env['purchase.order'].browse(self._context.get('active_ids', []))
        _logger.info("Eteration 0 %s",data)
        self.projet = False
        
        for m in data:
            self.projet = False
            _logger.info("Eteration 1 %s",m)
            m = [(3, self.id)]
            _logger.info("Eteration 2 %s",m)

    def action_delier_achat_t(self):
        raise ValidationError("hohohoho")





