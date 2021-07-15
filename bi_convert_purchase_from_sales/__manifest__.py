# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "Personnalisation convertion vente à achats ",
    'version' : "12.0.0.0",
    'category' : "Purchases",
    'summary': 'ce module lier les ventes et les achats',
    'description' : """
        Convert Purchase from Sales Order
        

     """,
    'author' : "Abdelghani KHALIDI",
    'website'  : "https://dkgroup.fr",
    'depends'  : [ 'base','sale_management','purchase'],
    'data'     : [  'security/ir.model.access.csv',
                    'wizard/purchase_order_wizard_view.xml',
                    'views/inherit_sale_order_view.xml',
            ],      
    'installable' : True,
    'application' :  False,
    "images":['static/description/Banner.png'],
}
