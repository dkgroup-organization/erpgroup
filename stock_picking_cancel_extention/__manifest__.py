# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Stock Picking Cancel - Extention',
    'version' : '1.0',
    'license' : 'OPL-1',
    'author': 'Vijay Dabhi',
    'summary' : 'Cancel "Done" Stock Picking',
    'description' : """
    Click Cancel sock picking when stage is "Done".
    """,
    'category': 'Warehouse',
    'images' : [],
    'depends' : ['stock'],
    'data': [
            'security/security.xml',
            'views/stock_picking_views.xml',
            ],
    'demo': [],
    "images":['static/description/icon.png'],
    'price':10,
    'currency':'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
}