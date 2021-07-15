# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": " ALL POS Reports in Odoo",
    "version": "12.0.0.0",
    "category": "Point of Sale",
    "depends": ['base', 'sale', 'point_of_sale'],
    "author": "BrowseInfo",
    'summary': 'Print POS Reports',
    "description": """
    print pos reports
    all in one pos reports
    point of sales reports
    pos reports 
    pos report

     pos sales summary report
     pos summary report
     pos Session and Inventory audit report
     pos audit report
     pos Product summary report
     pos sessions reports
     pos session reports
     pos User wise sales summary reports
     pos payment summary reports
     summary reports in POS
     point of sales summary reports
     point of sales reports
     pos user reports
     point of sales all reports
     pos products reports
     pos audit reports
     audit reports pos 


    pos Inventory audit reports
    pos Inventory reports
     Product summary report pos 



	""",
    "website": "www.browseinfo.in",
    "price": 39,
    "currency": "EUR",
    "data": [
        'views/pos_reports_assets.xml',
        'wizard/sales_summary_report.xml',
        'wizard/pos_sale_summary.xml',
        'wizard/x_report_view.xml',
        'wizard/z_report_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_reports.xml',
    ],
    "auto_install": False,
    "installable": True,
    "images": ['static/description/Banner.png'],
    "live_test_url": 'https://youtu.be/JjHQD5eMSBA',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
