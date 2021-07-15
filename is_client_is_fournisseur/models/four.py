# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError




class partner_client_four(models.Model):
    _inherit = 'res.partner'

    is_client = fields.Boolean("Est Client", default=False)
    is_fournisseur = fields.Boolean("Est Fournisseur", default=False)




    @api.onchange('is_client')
    def _onchange_is_client(self):

        if self.is_client == False and self.customer_rank != 0:
            self.customer_rank = 0
        if self.is_client == True and self.customer_rank == 0:
            self.cusotmer_rank = 1

    @api.onchange('is_fournisseur')
    def _onchange_is_fournisseur(self):

        if self.is_fournisseur == False and self.supplier_rank != 0:
            self.supplier_rank = 0
        if self.is_fournisseur == True and self.supplier_rank == 0:
            self.supplier_rank = 1



    @api.onchange('customer_rank')
    def _onchange_cusotumerrank(self):

        if self.is_client == False and self.customer_rank != 0:
            self.is_client = True
        if self.is_client == True and self.customer_rank == 0:
            self.is_client = False


    @api.onchange('supplier_rank')
    def _onchange_supplierrank(self):

        if self.is_fournisseur == False and self.supplier_rank != 0:
            self.is_fournisseur = True
        if self.is_fournisseur == True and self.supplier_rank == 0:
            self.is_fournisseur = False

    @api.model
    def create(self, values):
        res = super(partner_client_four, self).create(values)
        for m in self:
          if self.child_ids==[] and self.is_company == True:
            raise UserError(_("Ajouter un contact svp ! "))
        return res


    
    def write(self, values):
        res = super(partner_client_four, self).write(values)
        for m in self:
           if not m.child_ids and m.is_company == True:
            raise UserError(_("Ajouter un contact svp ! "))
        return res








   