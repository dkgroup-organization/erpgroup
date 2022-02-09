# -*- coding: utf-8 -*-
{
	'name':"Print Mass Invoices/Vendor Bills",
	'author':"Edge Technologies",
	'version':'14.0.1.0',
	'live_test_url': "https://youtu.be/rHU82zeDIls",
	"images":['static/description/main_screenshot.png'],
	'summary':"Generate Multiple PDF Invoices Print Mass Vendor Bills Print multiple Invoices print multiple Vendor Bills print mass invoice pdf report print mass vendor bill pdf print mass customer invoice generate mass pdf invoice generate bulk invoice pdf generate",
	'description': """
	Users can create Multiple Separate PDF invoices 
	through a Zip File without or with payment on a 
	Single Click. 
	""",
	"license" : "OPL-1",
	'depends':['base','account'],
	'data':[
		'security/ir.model.access.csv',
		'wizard/download_pdf.xml',
	],
	'installable':True,
	'auto_install':False,
	'price':12,
	'currency':'EUR',
	'category':'Accounting',			
}
