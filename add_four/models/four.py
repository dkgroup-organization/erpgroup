# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class addFour(models.Model):
    _inherit = 'account.move'


    fournisseur = fields.Many2one('res.partner',"Le Fournisseur", store=True,index=True,compute='_compute_name')
    

    @api.depends('invoice_line_ids')
    def _compute_name(self):
        for record in self:

            if record.invoice_line_ids: 
                if record.invoice_line_ids[0].product_id.seller_ids:                  
                 record.fournisseur= record.invoice_line_ids[0].product_id.seller_ids[0].name

                if len(record.invoice_line_ids)>1:
                   if record.invoice_line_ids[1].product_id.seller_ids: 
                     record.fournisseur= record.invoice_line_ids[1].product_id.seller_ids[0].name

            # elif record.invoice_line_ids and record.invoice_line_ids[2].product_id.seller_ids:

            #      record.fournisseur= record.invoice_line_ids[2].product_id.seller_ids[0].name
            else:

                 record.fournisseur= False
                      # = self.env['res.partner'].search([('name', '=', four)]).id
