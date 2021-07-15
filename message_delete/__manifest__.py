# -*- coding: utf-8 -*-
{
    "name": "Message Delete",
    "version": "13.0.1.2.1",
    "category": "Discuss",
    "author": "faOtools",
    "website": "https://faotools.com/apps/13.0/message-delete-398",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/templates.xml"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to let Odoo administrators delete messages from threads and channels",
    "description": """

For the full details look at static/description/index.html

- For message/notes editing use the tool &lt;a href='https://apps.odoo.com/apps/modules/13.0/message_edit/'&gt;Message / Note Editing&lt;/a&gt;

* Features * 

- In order to delete a message a user should just press the trash icon and confirm this action

- For security purposes the right to remove messages belongs only to the users with the right 'Settings &gt; Administration'
 
* Extra Notes *



    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "0.0",
    "currency": "EUR",
}