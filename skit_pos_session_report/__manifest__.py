# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Session Report',
    'version': '1.0',
    'author': 'Srikesh Infotech',
    'license': "AGPL-3",
    'website': 'http://www.srikeshinfotech.com',
    'sequence': 15,
    'summary': 'Session Report in Point of Sale screen',
    'description': """
Session Report In POS
==================================================================
This module allows to print the session report from
Point of Sale.

""",
    'images': ['images/main_screenshot.png'],
    'price': 15,
    'currency': 'EUR',
    'category': 'Point of sales',
    'depends': ['point_of_sale'],
    'qweb': ['static/src/xml/session_report.xml'],
    'data': ['views/pos_session_report_templates.xml',
             'report/pos_session_report_temp.xml',
             'report/pos_session_report.xml'],
   

    'installable': True,
    'auto_install': False,
    'application': True,
}
