from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"



    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(ResPartner, self).create(values)
 
        # Change the values of a variable in this super function
       
 
        # Return the record so that the changes are applied and everything is stored.
        return record


    @api.constrains('name')
    def _check_name(self):
     partner_rec = self.env['res.partner'].search(
        [('name', '=ilike', self.name),('company_id', '=ilike', self.company_id.name), ('id', '!=', self.id)])
     if partner_rec:
        raise ValueError(_('Ce contact est déja existe!'))


    @api.constrains('x_siren')
    def _check_siren(self):
     partner_rec = self.env['res.partner'].search(
        [('x_siren', '=ilike', self.x_siren), ('id', '!=', self.id)])
     if partner_rec:
        raise ValueError(_('Ce contact est déja existe!'))