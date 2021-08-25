# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "Liaison Project achats ventes",
    'version' : "13.0.0.0",
    'category' : "project",
    'summary': 'ce module lier les projects avec les ventes et les achats',
    'description' : """
        lier les projects avec les ventes et les achats
        

     """,
    'author' : "Abdelghani KHALIDI",
    'website'  : "https://dkgroup.fr",
    'depends'  : [ 'base','sale_management','purchase','account','project', 'mail', 'sale','sale_enterprise',"joint_piece",'mail', ],
    'data'     : [
                    'wizard/purchase_order_wizard_view.xml',
                    # 'views/inherit_sale_order_view.xml',
        "views/bouton_telephonique.xml"

       #  'views/assets.xml',
            ],      
    'installable' : True,
    'application' :  True,
    "images":['static/description/Banner.png'],
}
