# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _
import odoo.addons.decimal_precision as dp
class addfieldpurchasess(models.Model):
    _inherit = 'account.move'
    
    achats = fields.Many2many("purchase.order",'account_moveeeee_rel',string="Achats liés",copy=False) 
    montant_impact = fields.Float(string="Montant impacter sur l'achat",digits=dp.get_precision('Product Price'),store=True,copy=False )
    x_sellsy = fields.Boolean('sellsy',copy=False,store=True)

    @api.onchange('partner_id')
    def _onchange_partner(self):
    # set auto-changing field
       self.x_contact = False


class addfieldpurchasedd(models.Model):
    _inherit = 'purchase.order'
    vents_lies2 = fields.Many2many("sale.order",'accountt_move_rel',string="Ventes liés",copy=False) 
    vents_lies3 = fields.Many2many("account.move",'accountttt_move_rel',string="Facture liés",copy=False)  
    montant_impact = fields.Float(string="Montant impacter par des ventes",digits=dp.get_precision('Product Price'),copy=False )
    x_sellsy = fields.Boolean('sellsy',copy=False,store=True)

class addfieldpurchaseff(models.Model):
    _inherit = 'sale.order'
    vents_lies = fields.Many2many("purchase.order",'accounnnnt_move_rel',string="Ventes liés",copy=False)
    montant_impact = fields.Float(string="Montant impacter sur l'achat",digits=dp.get_precision('Product Price'),store=True,copy=False )
    x_sellsy = fields.Boolean('sellsy',copy=False,store=True)
