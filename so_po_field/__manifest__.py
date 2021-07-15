# -*- coding: utf-8 -*-
# Author: Red Lab.
# Copyright: Red Lab.

{
    'name': 'Purchase Order reference field in Sale Order form',
    'images': ['images/main_screenshot.png'],
    'version': '2.0.0',
    'category': 'Sales',
    'summary': 'Purchase Order field in Sale Order form',
    'author': 'Red Lab',
    'website': 'https://apps.odoo.com/apps/modules/browse?search=REDLAB',
    'depends': [
        'purchase',
        'sale',
    ],
    'data': [
        'views/sale_views.xml',
    ],
}
