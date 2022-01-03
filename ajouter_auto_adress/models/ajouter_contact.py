


from odoo import fields, models, api, _




class account(models.Model):
    _inherit = 'account.move'


    @api.model
    def create(self, values):
        sale_order = self.env['sale.order']
        self.x_contact = sale_order.partner_invoice_id
        # Add code here
        return super(account, self).create(values)