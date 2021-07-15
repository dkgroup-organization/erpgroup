# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "project_emmployes",
    'version' : "13.0.0.0",
    'category' : "Project",
    'summary': 'ce module pour la gestion des Project_employé',
    'description' : """
        Gestion Employes Project
        

     """,
    'author' : "Abdelghani KHALIDI",
    'website'  : "https://dkgroup.fr",
    'depends'  : [ 'base','hr','project'],
    'data'     : [  
                    'wizard/add_project_employees.xml',
                    # 'views/contacts_employees.xml',
                    # 'views/settings.xml',
                    # 'report/report.xml',
            ],      
    'installable' : True,
    'application' :  False,
    
}
