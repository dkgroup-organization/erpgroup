# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

# class addfieldpurchasess(models.Model):
#     _inherit = 'purchase.order'
    
#     cli = fields.Char(compute='_compute_name',index=True,copy=False,string="Client lié à cet achat",store=True)

#     @api.depends('vents_lies2','cli')
#     def _compute_name(self):
#         for record in self:
#             for m in record.vents_lies2:
#                 record.cli = m.partner_id.name




class MailComposer2(models.TransientModel):
   
    _inherit = 'mail.compose.message'
    company_id = fields.Many2one('res.company', 'Company', required=False, index=True, default=lambda self: self.env.company)


class categories(models.Model):
   
    _inherit = 'product.category'
    company_id = fields.Many2one('res.company', 'Company', required=False, index=True,store=True, default=lambda self: self.env.company)
    product_count = fields.Integer(
        '# Products', compute='_compute_product_count', store=True,index=True,
        help="The number of products under this category (Does not consider the children categories)")
    
    def action_company(self):
            res = self.env['product.template'].sudo().search([('categ_id', '=', self.id)])
            for j in res:
                   self.company_id = j.company_id.id

class Meeting2(models.Model):
   

    _inherit = 'calendar.event'
    company_id = fields.Many2one('res.company', 'Company', required=False, index=True, default=lambda self: self.env.company)

    
    def _company_compute(self):
      self.company_id = self.env.company.id

class AccountBankStatementLine2(models.Model):
    _inherit = "account.bank.statement.line"
    partner_id = fields.Many2one('res.partner', string='Partner', domain="[('x_company_ids', 'ilike', company_id)]" )

class AccountMoveLine2(models.Model):
    _inherit = "account.move.line"
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict', domain="[('x_company_ids', 'ilike', company_id)]")