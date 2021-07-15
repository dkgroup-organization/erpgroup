# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'All In One Cancel Sales,Purchases and Delivery,Invoice',
    'version' : '1.0',
    'author':'Craftsync Technologies',
    'category': 'Sales',
    'maintainer': 'Craftsync Technologies',
    'summary': """ all in one cancel  ALL IN ONE CANCEL  all cancel  all in one All In One  ALL IN ONE
        All Cancel all sale cancel all cancel order sale purchase delivery picking invoice sales cancel 
        cancel sales cancel purchase cancel delivery cancel sale cancel puchases cancel order 
        all in one order cancel invoice cancel bill bill cancel invoice cancel picking 
        cancel delivery cancel purcahse cancel sale order cancel delivery order cancel sales order 
        cancel delivery orders cancel bills cancel invoices cancel sales Cancel Cancel sales 
        Cancel purchase Cancel delivery Cancel sale Cancel puchases Cancel order 
        all in one order Cancel invoice Cancel bill bill Cancel invoice Cancel picking Cancel delivery Cancel 
        purcahse Cancel sale order Cancel delivery order Cancel sales order Cancel delivery orders Cancel bills 
        Cancel invoices Cancel Sale Purchase Delivery Picking Invoice Sales Cancel Cancel Sales Cancel Purchase 
        Cancel Delivery Cancel Sale Cancel Puchases Cancel Order Cancel Orders All In One Order All In One Orders 
        Cancel Invoice Cancel Bill Bill Cancel Invoice Cancel Picking Cancel Delivery Cancel purcahse 
        Cancel Sale Order Cancel Delivery Order Cancel Sales Order Cancel Delivery Orders Cancel Bills Cancel Invoices Cancel  
    """,

    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'depends' : ['purchase_stock','sale_management','sale_stock'],
    'data': [

        'views/res_config_settings_views.xml',
        'views/view_purchase_order.xml',
        'views/stock_warehouse.xml',
        'views/view_sale_order.xml',
        'views/stock_picking.xml',
        'wizard/view_cancel_invoice_wizard.xml',
        'views/invoice.xml',
        'wizard/view_cancel_delivery_wizard.xml',

    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 34.99,
    'currency': 'EUR',

    'images': ['static/description/main_screen.png'],

}
