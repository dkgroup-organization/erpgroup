# -*- coding: utf-8 -*-
# Author: Red Lab.
# Copyright: Red Lab.

{
    'name': 'Sale Order reference field in Purchase Order form',
    'images': ['images/main_screenshot.png'],
    'version': '2.0.0',
    'category': 'Purchases',
    'summary': 'Sale order field in Purchase Order/RFQ form',
    'author': 'Red Lab',
    'website': 'https://apps.odoo.com/apps/modules/browse?search=REDLAB',
    'depends': [
        'sale',
        'purchase',
    ],
    'data': [
        'views/purchase_views.xml',
    ],
}
