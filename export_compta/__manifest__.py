# See LICENSE file for full copyright and licensing details.

{
    "name": "Export Account move line",
    "version": "13.0.1.0.0",
    "category": "Account",
    "license": "AGPL-3",
    "summary": "Export account move line to CEGID",
    "author": "DKgroup",
    "website": "http://www.dkgroup.fr",
    "maintainer": "DKGROUP",
    "images": [],
    "depends": [
        "base", "account",
    ],
    "data": [
        "view/menu_export_compta.xml",
        
        "view/res_partner.xml",
        "view/account_journal.xml",
        "view/account_account.xml",

        #"view/account_move.xml",
        "view/view_export_history.xml",
        "view/wizard_account_export_line.xml",

        "security/ir.model.access.csv"

    ],
    "installable": True,
}
