# coding: utf-8
{
    'name': "Import CSV Data",
    'summary': """
                   Import CSV Data
     """,

    'description': """
        Import CSV Data
    """,

    'author': "DK GROUP",
    'website': "",
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'sale', 'purchase', 'stock', 'account', 'export_compta'

    ],
    # always loaded
    'data': [
        "wizards/import_data_views.xml",
        "security/ir.model.access.csv",
    ],
    # only loaded in demonstration mode
    'demo': [],
}
