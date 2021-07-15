# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import xml.etree.ElementTree as xee
from odoo import api, models, fields, _

class PersoFields(models.Model):
    _inherit = 'ir.model.fields'
    # pdf = fields.Boolean('afficher dans les document ?')
    model = fields.Selection([('sale.order', 'Devis'),
                                 ('account.invoice', 'Facture'),('purchase.order', 'Demande de prix'),('product.template', 'Article'),('res.partner', 'Client')], string='Modéle', required=True)




   


    @api.model
    def create(self, values):
        
        r = super(PersoFields, self).create(values)
        
       
        if r.model == 'sale.order':
         inherit_id = self.env.ref('sale.view_order_form')
         arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="validity_date" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (r.name)
         self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
                                              'type': 'form',
                                              'model': 'sale.order',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
         if r.x_display_pdf == True:
          inherit_id2 = self.env.ref('sale.report_saleorder_document')
          arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="perso" class="col-auto mw-100 mb-2" position="after">'
                      '<p t-if="doc.%s">%s : '
                      '<span class="m-0" t-field="doc.%s"/> </p>'      
                      '</div>'
                      '</data>') % (r.name,r.field_description,r.name)

          self.env['ir.ui.view'].sudo().create({'name': r.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})


         

        if r.model == 'account.invoice':
         inherit_id = self.env.ref('account.invoice_form')
         arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_invoice" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (r.name)
         self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
                                              'type': 'form',
                                              'model': 'account.invoice',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
         if r.x_display_pdf == True:
          inherit_id2 = self.env.ref('account.report_invoice_document')
          arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="addchamps" class="col-auto mw-100 mb-2" position="after">' 
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (r.name,r.field_description,r.name)

          self.env['ir.ui.view'].sudo().create({'name': r.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True}) 







        if r.model == 'purchase.order':
         inherit_id = self.env.ref('purchase.purchase_order_form')
         arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_order" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (r.name)
         self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
                                              'type': 'form',
                                              'model': 'purchase.order',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
         if r.x_display_pdf == True:
          inherit_id2 = self.env.ref('purchase.report_purchaseorder_document')
          arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      ' <div name="perso" class="m-0" position="after">'
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (r.name,r.field_description,r.name)

          self.env['ir.ui.view'].sudo().create({'name': r.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})  

        if r.model == 'product.template':
         inherit_id = self.env.ref('product.product_template_only_form_view')
         arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="uom_po_id" position="after">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (r.name)
         self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
                                              'type': 'form',
                                              'model': 'product.template',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        if r.model == 'res.partner':
         inherit_id = self.env.ref('base.view_partner_form')
         arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="category_id" position="after">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (r.name)
         self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
                                              'type': 'form',
                                              'model': 'res.partner',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})
        return r


    def unlink(self):
        for u in self:
         self.env['ir.ui.view'].search([('name','=',u.name+'vvv')]).sudo().unlink()
         self.env['ir.ui.view'].search([('name','=',u.name)]).sudo().unlink()

        return super(PersoFields, self).unlink()




    # def write(self,values):
    #     for k in self:
    #      self.env['ir.ui.view'].search([('name','=',k.name+'vvv')]).sudo().unlink()
    #      self.env['ir.ui.view'].search([('name','=',k.name)]).sudo().unlink()

    #     k = super(PersoFields,self).write(values)
        
    #     if self.model == 'sale.order':
    #      inherit_id = self.env.ref('sale.view_order_form')
    #      arch_base = _('<?xml version="1.0"?>'
    #                   '<data>'
    #                   '<field name="validity_date" position="before">'
    #                   '<field name="%s"/>'
    #                   '</field>'
    #                   '</data>') % (self.name)
    #      self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
    #                                           'type': 'form',
    #                                           'model': 'sale.order',
    #                                           'mode': 'extension',
    #                                           'inherit_id': inherit_id.id,
    #                                           'arch_base': arch_base,
    #                                           'active': True})

        
    #      if self.x_display_pdf == True:
    #       inherit_id2 = self.env.ref('sale.report_saleorder_document')
    #       arch_base2 = _('<?xml version="1.0"?>'
    #                   '<data>'  
    #                   '<div name="perso" class="col-auto mw-100 mb-2" position="after">'
    #                   '<p t-if="doc.%s">%s : '
    #                   '<span class="m-0" t-field="doc.%s"/> </p>'      
    #                   '</div>'
    #                   '</data>') % (self.name,self.field_description,self.name)

    #       self.env['ir.ui.view'].sudo().create({'name': self.name,
    #                                           'mode': 'extension',
    #                                           'type': 'qweb',
    #                                           'inherit_id': inherit_id2.id,
    #                                           'arch_base': arch_base2,
    #                                           'active': True})



    #     if self.model == 'account.invoice':
    #      inherit_id = self.env.ref('account.invoice_form')
    #      arch_base = _('<?xml version="1.0"?>'
    #                   '<data>'
    #                   '<field name="date_invoice" position="before">'
    #                   '<field name="%s"/>'
    #                   '</field>'
    #                   '</data>') % (self.name)
    #      self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
    #                                           'type': 'form',
    #                                           'model': 'account.invoice',
    #                                           'mode': 'extension',
    #                                           'inherit_id': inherit_id.id,
    #                                           'arch_base': arch_base,
    #                                           'active': True})

        
    #      if self.x_display_pdf == True:
    #       inherit_id2 = self.env.ref('account.report_invoice_document')
    #       arch_base2 = _('<?xml version="1.0"?>'
    #                   '<data>'  
    #                   '<div name="addchamps" class="col-auto mw-100 mb-2" position="after">' 
    #                   '<p t-if="o.%s">%s : '
    #                   '<span class="m-0" t-field="o.%s"/> </p>'      
    #                   '</div>'
    #                   '</data>') % (self.name,self.field_description,self.name)

    #       self.env['ir.ui.view'].sudo().create({'name': self.name,
    #                                           'mode': 'extension',
    #                                           'type': 'qweb',
    #                                           'inherit_id': inherit_id2.id,
    #                                           'arch_base': arch_base2,
    #                                           'active': True}) 







    #     if self.model == 'purchase.order':
    #      inherit_id = self.env.ref('purchase.purchase_order_form')
    #      arch_base = _('<?xml version="1.0"?>'
    #                   '<data>'
    #                   '<field name="date_order" position="before">'
    #                   '<field name="%s"/>'
    #                   '</field>'
    #                   '</data>') % (self.name)
    #      self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
    #                                           'type': 'form',
    #                                           'model': 'purchase.order',
    #                                           'mode': 'extension',
    #                                           'inherit_id': inherit_id.id,
    #                                           'arch_base': arch_base,
    #                                           'active': True})

        
    #      if self.x_display_pdf == True:
    #       inherit_id2 = self.env.ref('purchase.report_purchaseorder_document')
    #       arch_base2 = _('<?xml version="1.0"?>'
    #                   '<data>'  
    #                   ' <div name="perso" class="m-0" position="after">'
    #                   '<p t-if="o.%s">%s : '
    #                   '<span class="m-0" t-field="o.%s"/> </p>'      
    #                   '</div>'
    #                   '</data>') % (self.name,self.field_description,self.name)

    #       self.env['ir.ui.view'].sudo().create({'name': self.name,
    #                                           'mode': 'extension',
    #                                           'type': 'qweb',
    #                                           'inherit_id': inherit_id2.id,
    #                                           'arch_base': arch_base2,
    #                                           'active': True})  

    #     if self.model == 'product.template':
    #      inherit_id = self.env.ref('product.product_template_only_form_view')
    #      arch_base = _('<?xml version="1.0"?>'
    #                   '<data>'
    #                   '<field name="uom_po_id" position="after">'
    #                   '<field name="%s"/>'
    #                   '</field>'
    #                   '</data>') % (self.name)
    #      self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
    #                                           'type': 'form',
    #                                           'model': 'product.template',
    #                                           'mode': 'extension',
    #                                           'inherit_id': inherit_id.id,
    #                                           'arch_base': arch_base,
    #                                           'active': True})

    #     if self.model == 'res.partner':
    #      inherit_id = self.env.ref('base.view_partner_form')
    #      arch_base = _('<?xml version="1.0"?>'
    #                   '<data>'
    #                   '<field name="category_id" position="after">'
    #                   '<field name="%s"/>'
    #                   '</field>'
    #                   '</data>') % (self.name)
    #      self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
    #                                           'type': 'form',
    #                                           'model': 'res.partner',
    #                                           'mode': 'extension',
    #                                           'inherit_id': inherit_id.id,
    #                                           'arch_base': arch_base,
    #                                           'active': True})
    #     return k