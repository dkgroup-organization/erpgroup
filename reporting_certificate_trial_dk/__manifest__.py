# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "DK Group Reporting",
    'version': "14.0.1.0.0",
    'category': "Project",
    'summary': 'ce module pour la gestion des attestation des travaux et proces verbal',
    'description': """
        Les rapport des attestions de travaux et les proces verbal .


     """,
    'author': "KHALLOUT Asmaa",
    'website': "https://dkgroup.fr",
    'depends': ['project_liaison'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_inherit_view.xml',
        'wizard/report_certificate_view.xml'
    ],
    'installable': True,
    'application': True,

}
