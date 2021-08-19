# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "AMB CUSTOM PROJECT LIASON",
    'version': "14.0.1.0.0",
    'category': "Project",
    'summary': 'ce module pour la gestion la liason entre facture vente achat et projet',
    'description': """
        Projet


     """,
    'author': "KHALLOUT Asmaa",
    'website': "https://dkgroup.fr",
    'depends': ['base','amb_custom_vente_achat_projet'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'wizard/sale_order_wizard_views.xml',
        # 'wizard/purchase_order_wizard_views.xml',
        # 'wizard/account_move_wizard_views.xml',
        # 'views/project_project_inherit_view.xml',
        # 'views/sale_order_inherit_view.xml',
        # 'views/purchase_order_inherit_view.xml',
        # 'views/account_move_inherit_view.xml',
        # 'report/report_saleorder_document_report_inherit.xml',
        # 'report/report_purchaseorder_document_inherit.xml',
        'security/ir.model.access.csv',
        'report/report_work_certificate.xml',
        'report/report_verbal_trial.xml',
        'wizard/views.xml',
        'views/project_project_inherit_view.xml',
        'views/account_move_inherit_view.xml',
        'views/res_partner_inherit_view.xml',
        'views/res_config_settings_inherit_view.xml',
        'views/sale_order_inherit_view.xml',
        'views/res_partner_customer_statements_inherit.xml',
        'wizard/report_certificate_view.xml'
    ],
    'installable': True,
    'application': True,

}
