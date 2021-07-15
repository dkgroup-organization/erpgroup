# -*- coding: utf-8 -*-

import xml.etree.ElementTree as xee

from odoo import api, models, fields, _


class EmployeeDynamicFields(models.TransientModel):
    _name = 'wizard.dynamic.fields'
    _description = 'Dynamic Fields'
    _inherit = 'ir.model.fields'

    @api.model
    def get_field_types(self):
        field_list = sorted((key, key) for key in fields.MetaField.by_type)
        field_list.remove(('one2many', 'one2many'))
        field_list.remove(('reference', 'reference'))
        return field_list

    def _set_default(self):
        model_id = self.env['ir.model'].sudo().search([('model', '=', 'sale.order')])
        return [('id', '=', model_id.id)]
    def create_fields(self):
     if self.trans == False:
      self.env['ir.model.fields'].sudo().create({'name': self.name,
                                                   'field_description': self.field_description,
                                                   'model_id': self.model_id,
                                                   'ttype': self.ttype,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'active': True,
                                                   'x_display_pdf': self.display_pdf})

      if self.model_id == 333:
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

        
         if self.display_pdf == True:
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


         

      if self.model_id == 227:
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

        
         if self.display_pdf == True:
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







      if self.model_id == 278:
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

        
         if r.display_pdf == True:
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

      if self.model_id == 197:
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

      if self.model_id == 74:
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
      self.env['ir.model.fields'].sudo().create({'name': self.name,
                                                   'field_description': self.field_description,
                                                   'model_id': 333,
                                                   'x_trans' : True,
                                                   'x_display_pdf' : self.display_pdf,
                                                   'ttype': self.ttype,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'active': True})
      self.env['ir.model.fields'].sudo().create({'name': self.name,
                                                   'field_description': self.field_description,
                                                   'model_id': 227,
                                                   'x_show': True,
                                                   'ttype': self.ttype,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'related': 'x_sale_id.'+self.name,
                                                   'active': True})
      self.env['ir.model.fields'].sudo().create({'name': self.name,
                                                   'field_description': self.field_description,
                                                   'model_id': 278,
                                                   'ttype': self.ttype,
                                                   'x_show': True,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'active': True})

      self.env['ir.model.fields'].sudo().create({'name': self.name+'_fourniss',
                                                   'field_description': self.field_description,
                                                   'model_id': 227,
                                                   'ttype': self.ttype,
                                                   'x_show': True,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'related': 'x_purchase_id.'+self.name,
                                                   'active': True})
      self.env['ir.model.fields'].sudo().create({'name': self.name+'_avr',
                                                   'field_description': self.field_description,
                                                   'model_id': 227,
                                                   'x_show': True,
                                                   'ttype': self.ttype,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'related': 'refund_invoice_id.'+self.name,
                                                   'active': True})
      self.env['ir.model.fields'].sudo().create({'name': self.name+'_avrf',
                                                   'field_description': self.field_description,
                                                   'model_id': 227,
                                                   'x_show': True,
                                                   'ttype': self.ttype,
                                                   'required': self.required,
                                                   'selection': self.selection,
                                                   'copy': self.copy,
                                                   'related': 'refund_invoice_id.'+self.name+'_fourniss',
                                                   'active': True})
      

      
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

        
      if self.display_pdf == True:
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
                      '<field name="%s" attrs="{\'invisible\': [\'|\',(\'type\',\'=\',\'in_refund\'),(\'type\',\'=\',\'out_refund\')]}"/>'
                      '</field>'
                      '</data>') % (self.name)
      self.env['ir.ui.view'].sudo().create({'name': self.name+'vvv',
                                              'type': 'form',
                                              'model': 'account.invoice',
                                              'mode': 'extension',
                                              'inherit_id': inherit_id.id,
                                              'arch_base': arch_base,
                                              'active': True})
      inherit_id = self.env.ref('account.invoice_form')
      arch_base = _('<?xml version="1.0"?>'
                      '<data>'
                      '<field name="date_invoice" position="before">'
                      '<field name="%s"  attrs="{\'invisible\': [(\'type\',\'!=\',\'out_refund\')]}"/>'
                      '</field>'
                      '</data>') % (self.name+'_avr')
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

        
      if self.display_pdf == True:
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









      
    

         

     return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

   
    trans = fields.Boolean('est transvesale ?')
    display_pdf = fields.Boolean('Afficher dans le document ?')
    model_id = fields.Selection([(333, 'Devis'),
                                 (227, 'Facture'),(278, 'Demande de prix'),(197, 'Article'),(74, 'Client')], string='Modéle', required=True)
    ref_model_id = fields.Many2one('ir.model', string='Model', index=True)
    rel_field = fields.Many2one('ir.model.fields', string='Related Field')
    ttype = fields.Selection(selection='get_field_types', string='Field Type', required=True)
