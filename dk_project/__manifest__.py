# -*- coding: utf-8 -*-
{
    'name': "DK Project",

    'summary': """
        DK Project""",

    'description': """
        DK Project
    """,

    'author': "DK Group",
    'website': "https://www.dkgroup.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'project',
        'planning',
        'sale_timesheet_enterprise',
        'helpdesk',
        'hr_timesheet',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/helpdesk_ticket_views.xml',
        # 'views/templates.xml',
        # 'views/assets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'sequence': -50
}
