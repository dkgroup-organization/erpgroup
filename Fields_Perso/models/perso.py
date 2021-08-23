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
    x_trans = fields.Boolean('Champ Transversal')




    # def create_fields(self):
    #      self.env['ir.model.fields'].sudo().create({ 'model_id': 227,
    #                                                 'name': 'x_selfname222222',
    #                                                 'field_description': 'selffield_description',
    #                                                 'ttype': 'char',
    #                                                 'active': True})


    # def create(self, values):

    #     values = [{ 'model_id': 227,
    #                                                 'name': 'x_selfname222222',
    #                                                 'field_description': 'selffield_description',
    #                                                 'ttype': 'char',
    #                                                 'active': True}, { 'model_id': 333,
    #                                                 'name': 'x_selfname222222',
    #                                                 'field_description': 'selffield_description',
    #                                                 'ttype': 'char',
    #                                                 'active': True}, { 'model_id': 227,
    #                                                 'name': 'x_selfname33',
    #                                                 'field_description': 'selffield_description',
    #                                                 'ttype': 'char',
    #                                                 'active': True}]

    #     self.env['ir.model.fields'].sudo().create(values)
        # r = super(PersoFields, self).create(values)
        
        # r = super(PersoFields, self).create(values)
        
       
        # if r.model == 'sale.order':
        #  inherit_id = self.env.ref('sale.view_order_form')
        #  arch_base = _('<?xml version="1.0"?>'
        #               '<data>'
        #               '<field name="validity_date" position="before">'
        #               '<field name="%s"/>'
        #               '</field>'
        #               '</data>') % (r.name)
        #  self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
        #                                       'type': 'form',
        #                                       'model': 'sale.order',
        #                                       'mode': 'extension',
        #                                       'inherit_id': inherit_id.id,
        #                                       'arch_base': arch_base,
        #                                       'active': True})

        
        #  if r.x_display_pdf == True:
        #   inherit_id2 = self.env.ref('sale.report_saleorder_document')
        #   arch_base2 = _('<?xml version="1.0"?>'
        #               '<data>'  
        #               '<div name="perso" class="col-auto mw-100 mb-2" position="after">'
        #               '<p t-if="doc.%s">%s : '
        #               '<span class="m-0" t-field="doc.%s"/> </p>'      
        #               '</div>'
        #               '</data>') % (r.name,r.field_description,r.name)

        #   self.env['ir.ui.view'].sudo().create({'name': r.name,
        #                                       'mode': 'extension',
        #                                       'type': 'qweb',
        #                                       'inherit_id': inherit_id2.id,
        #                                       'arch_base': arch_base2,
        #                                       'active': True})


         

        # if r.model == 'account.invoice':
        #  inherit_id = self.env.ref('account.invoice_form')
        #  arch_base = _('<?xml version="1.0"?>'
        #               '<data>'
        #               '<field name="date_invoice" position="before">'
        #               '<field name="%s"/>'
        #               '</field>'
        #               '</data>') % (r.name)
        #  self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
        #                                       'type': 'form',
        #                                       'model': 'account.invoice',
        #                                       'mode': 'extension',
        #                                       'inherit_id': inherit_id.id,
        #                                       'arch_base': arch_base,
        #                                       'active': True})

        
        #  if r.x_display_pdf == True:
        #   inherit_id2 = self.env.ref('account.report_invoice_document')
        #   arch_base2 = _('<?xml version="1.0"?>'
        #               '<data>'  
        #               '<div name="addchamps" class="col-auto mw-100 mb-2" position="after">' 
        #               '<p t-if="o.%s">%s : '
        #               '<span class="m-0" t-field="o.%s"/> </p>'      
        #               '</div>'
        #               '</data>') % (r.name,r.field_description,r.name)

        #   self.env['ir.ui.view'].sudo().create({'name': r.name,
        #                                       'mode': 'extension',
        #                                       'type': 'qweb',
        #                                       'inherit_id': inherit_id2.id,
        #                                       'arch_base': arch_base2,
        #                                       'active': True}) 







        # if r.model == 'purchase.order':
        #  inherit_id = self.env.ref('purchase.purchase_order_form')
        #  arch_base = _('<?xml version="1.0"?>'
        #               '<data>'
        #               '<field name="date_order" position="before">'
        #               '<field name="%s"/>'
        #               '</field>'
        #               '</data>') % (r.name)
        #  self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
        #                                       'type': 'form',
        #                                       'model': 'purchase.order',
        #                                       'mode': 'extension',
        #                                       'inherit_id': inherit_id.id,
        #                                       'arch_base': arch_base,
        #                                       'active': True})

        
        #  if r.x_display_pdf == True:
        #   inherit_id2 = self.env.ref('purchase.report_purchaseorder_document')
        #   arch_base2 = _('<?xml version="1.0"?>'
        #               '<data>'  
        #               ' <div name="perso" class="m-0" position="after">'
        #               '<p t-if="o.%s">%s : '
        #               '<span class="m-0" t-field="o.%s"/> </p>'      
        #               '</div>'
        #               '</data>') % (r.name,r.field_description,r.name)

        #   self.env['ir.ui.view'].sudo().create({'name': r.name,
        #                                       'mode': 'extension',
        #                                       'type': 'qweb',
        #                                       'inherit_id': inherit_id2.id,
        #                                       'arch_base': arch_base2,
        #                                       'active': True})  

        # if r.model == 'product.template':
        #  inherit_id = self.env.ref('product.product_template_only_form_view')
        #  arch_base = _('<?xml version="1.0"?>'
        #               '<data>'
        #               '<field name="uom_po_id" position="after">'
        #               '<field name="%s"/>'
        #               '</field>'
        #               '</data>') % (r.name)
        #  self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
        #                                       'type': 'form',
        #                                       'model': 'product.template',
        #                                       'mode': 'extension',
        #                                       'inherit_id': inherit_id.id,
        #                                       'arch_base': arch_base,
        #                                       'active': True})

        # if r.model == 'res.partner':
        #  inherit_id = self.env.ref('base.view_partner_form')
        #  arch_base = _('<?xml version="1.0"?>'
        #               '<data>'
        #               '<field name="category_id" position="after">'
        #               '<field name="%s"/>'
        #               '</field>'
        #               '</data>') % (r.name)
        #  self.env['ir.ui.view'].sudo().create({'name': r.name+'vvv',
        #                                       'type': 'form',
        #                                       'model': 'res.partner',
        #                                       'mode': 'extension',
        #                                       'inherit_id': inherit_id.id,
        #                                       'arch_base': arch_base,
        #                                       'active': True})


        # return r
    def unlinkoo(self):
     for u in self:
      self.env['ir.ui.view'].search([('name','=',u.name+'vvv')]).sudo().unlink()
      self.env['ir.ui.view'].search([('name','=',u.name+'vvvavr')]).sudo().unlink()
      self.env['ir.ui.view'].search([('name','=',u.name+'fourniss')]).sudo().unlink()
      self.env['ir.ui.view'].search([('name','=',u.name)]).sudo().unlink()
      self.env['ir.model.fields'].search([('name','=',u.name+'_avr')]).sudo().unlink()
      self.env['ir.model.fields'].search([('name','=',u.name+'_avrf')]).sudo().unlink()
      self.env['ir.model.fields'].search([('name','=',u.name+'_fourniss')]).sudo().unlink()
      self.env['ir.model.fields'].search([('name','=',u.name),('model','=','account.invoice')]).sudo().unlink()
      self.env['ir.model.fields'].search([('name','=',u.name)]).sudo().unlink()
#      return {
#        'name': _('ir.model.fields tree'),
#        'view_type': 'form',
#        'view_mode': 'tree',
#        'view_id': self.env.ref('base.view_model_fields_tree').id,
#        'res_model': 'ir.model.fields',
#        'type': 'ir.actions.act_window',
#        'domain': '["&","&",["state","=","manual"],"|","|","|",["model_id","ilike","commande"],["model_id","ilike","facture"],["model_id","ilike","article"],["model_id","ilike","contact"],["x_show","!=",True]]',
#        'target': 'current',
# }

    def unlink(self):
     for u in self:
       self.env['ir.ui.view'].search([('name','=',u.name+'vvv')]).sudo().unlink()
       self.env['ir.ui.view'].search([('name','=',u.name)]).sudo().unlink()
     return super(PersoFields, self).unlink()




    def write(self,values):
        for k in self:
         self.env['ir.ui.view'].search([('name','=',k.name+'vvv')]).sudo().unlink()
         self.env['ir.ui.view'].search([('name','=',k.name+'vvvavr')]).sudo().unlink()
         self.env['ir.ui.view'].search([('name','=',k.name+'fourniss')]).sudo().unlink()
         self.env['ir.ui.view'].search([('name','=',k.name)]).sudo().unlink()

        k = super(PersoFields,self).write(values)
        if self.x_trans == False:
         if self.model == 'sale.order':
          inherit_id = self.env.ref('sale.view_order_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="validity_date" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'sale.order',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.x_display_pdf == True:
           inherit_id2 = self.env.ref('sale.report_saleorder_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="perso" class="col-auto mw-100 mb-2" position="after">'
                      '<p t-if="doc.%s">%s : '
                      '<span class="m-0" t-field="doc.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name,self.field_description,self.name)

           self.env['ir.ui.view'].sudo().create({'name': self.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})



         if self.model == 'account.invoice':
          inherit_id = self.env.ref('account.invoice_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_invoice" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'account.invoice',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.x_display_pdf == True:
           inherit_id2 = self.env.ref('account.report_invoice_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="addchamps" class="col-auto mw-100 mb-2" position="after">' 
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name,self.field_description,self.name)

           self.env['ir.ui.view'].sudo().create({'name': self.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True}) 







         if self.model == 'purchase.order':
          inherit_id = self.env.ref('purchase.purchase_order_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_order" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'purchase.order',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.x_display_pdf == True:
           inherit_id2 = self.env.ref('purchase.report_purchaseorder_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      ' <div name="perso" class="m-0" position="after">'
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name,self.field_description,self.name)

           self.env['ir.ui.view'].sudo().create({'name': self.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})  

         if self.model == 'product.template':
          inherit_id = self.env.ref('product.product_template_only_form_view')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="uom_po_id" position="after">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'product.template',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

         if self.model == 'res.partner':
          inherit_id = self.env.ref('base.view_partner_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="category_id" position="after">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'res.partner',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})
        
        else:
          inherit_id = self.env.ref('sale.view_order_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="validity_date" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'sale.order',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.x_display_pdf == True:
           inherit_id2 = self.env.ref('sale.report_saleorder_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="perso" class="col-auto mw-100 mb-2" position="after">'
                      '<p t-if="doc.%s">%s : '
                      '<span class="m-0" t-field="doc.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name,self.field_description,self.name)

           self.env['ir.ui.view'].sudo().create({'name': self.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})



        
          inherit_id = self.env.ref('account.invoice_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_invoice" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'account.invoice',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.x_display_pdf == True:
           inherit_id2 = self.env.ref('account.report_invoice_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="addchamps" class="col-auto mw-100 mb-2" position="after">' 
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name,self.field_description,self.name)

           self.env['ir.ui.view'].sudo().create({'name': self.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True}) 



         
          inherit_id = self.env.ref('purchase.purchase_order_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_order" position="before">'
                      '<field name="%s"/>'
                      '</field>'
                      '</data>') % (self.name)
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'purchase.order',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.x_display_pdf == True:
           inherit_id2 = self.env.ref('purchase.report_purchaseorder_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      ' <div name="perso" class="m-0" position="after">'
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name,self.field_description,self.name)

           self.env['ir.ui.view'].sudo().create({'name': self.name,
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})
          inherit_id = self.env.ref('account.invoice_supplier_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="origin" position="before" >'
                      '<field name="%s" attrs="{\'invisible\': [(\'type\',\'=\',\'in_refund\')]}"/>'
                      '</field>'
                      '</data>') % (self.name+'_fourniss')
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'account.invoice',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})
          inherit_id = self.env.ref('account.invoice_supplier_form')
          arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="origin" position="before" >'
                      '<field name="%s" attrs="{\'invisible\': [(\'type\',\'!=\',\'in_refund\')]}"/>'
                      '</field>'
                      '</data>') % (self.name+'_avrf')
          self.env['ir.ui.view'].sudo().create({'name': self.name+'vvvavr',
                                              'type': 'form',
                                              'model': 'account.invoice',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})

        
          if self.display_pdf == True:
           inherit_id2 = self.env.ref('account.report_invoice_document')
           arch_base2 = _('<?xml version="1.0"?>'
                      '<data>'  
                      '<div name="addchamps" class="col-auto mw-100 mb-2" position="after">' 
                      '<p t-if="o.%s">%s : '
                      '<span class="m-0" t-field="o.%s"/> </p>'      
                      '</div>'
                      '</data>') % (self.name+'_fourniss',self.field_description,self.name+'_fourniss')

           self.env['ir.ui.view'].sudo().create({'name': self.name+'_fourniss',
                                              'mode': 'extension',
                                              'type': 'qweb',
                                              'inherit_id': inherit_id2.id,
                                              'arch_base': arch_base2,
                                              'active': True})  


        return k