# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from datetime import datetime,date
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError




class saleorderadd(models.Model):
    _inherit = 'sale.order'

    numero_commande = fields.Char('Numéro de bon de commande')
    required_numero_commande = fields.Boolean( string="Joindre au Mail",default=False,compute='_computerequired')


    @api.depends('partner_id')
    def _computerequired(self):
        for m in self:
            m.required_numero_commande = m.partner_id.bcd_exige




class saleorderadd(models.Model):
    _inherit = 'account.move'

    numero_commande = fields.Char('Numéro de bon de commande')

    required_numero_commande = fields.Boolean( string="Joindre au Mail",default=False,compute='_computerequired')


    @api.depends('partner_id')
    def _computerequired(self):
        for m in self:
            m.required_numero_commande = m.partner_id.bcd_exige





class saleorderadd(models.Model):
    _inherit = 'res.partner'

    date_garantie = fields.Date("Date de Garantie", store=True,default=False)


    @api.onchange('montant_garantie')
    def change_date(self):
        if self.montant_garantie != 0.0:
           self.date_garantie = date.today().strftime('%Y-%m-%d')
        
        
    @api.onchange('siret')
    def delete_space_siret(self):
        if self.siret:
           self.siret.replace(" ","")

   
