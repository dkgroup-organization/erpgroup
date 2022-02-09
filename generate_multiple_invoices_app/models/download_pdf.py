# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import base64
from zipfile import ZipFile
import io
import os

class WizardMultipleInv(models.TransientModel):
	_name = 'wizard.download.pdf'
	_description='Download PDF'

	pdf_report = fields.Selection([('invoice','Invoice'),
			('inv_payment','Invoice Without Payment')],
			'PDF Report',required=True)
	state = fields.Selection([('draft','Draft'),
			('done','Done')],
			'Stage',default= 'draft')
	download_pdf_report = fields.Binary('Download PDF Report',
		readonly=True)
	file_name = fields.Char(string='Name')


	def wizard_binary(self):
		list1 = []
		if self.pdf_report == 'inv_payment':
			var = 0
			for active_ids in self.env['account.move'].browse(self._context.get('active_ids')):
				pdf = self.env.ref('account.account_invoices').render_qweb_pdf(active_ids.id)[0]
				list1.append(active_ids)
				
				if active_ids.name == '/':
					var += 1
					with open('/tmp/' +(active_ids.name).replace('/','_') + "%s.pdf" % (var), "wb") as outfile:
						outfile.write(pdf)
				else:
					with open('/tmp/' +(active_ids.name).replace('/','_') + ".pdf", "wb") as outfile:
						outfile.write(pdf)

			with ZipFile('allpdffiles.zip', 'w') as myzip:
				var2 = 0
				for order in list1:
					if order.name == '/':
						var2 += 1
						myzip.write('/tmp/' +(order.name).replace('/','_') + "%s.pdf" % (var2))
					else:
						myzip.write('/tmp/' +(order.name).replace('/','_') + ".pdf")
			
			with open("allpdffiles.zip", "rb") as f:
				converts = f.read()
				encoded = base64.b64encode(converts)

			self.file_name = 'Invoices Without Payment.zip'	
			self.download_pdf_report = encoded

			var3 = 0
			for result in list1:
				if result.name == '/':
					var3 += 1
					os.remove('/tmp/' +(result.name).replace('/','_') + "%s.pdf" % (var3))
				else:
					os.remove('/tmp/' +(result.name).replace('/','_') + ".pdf")

			os.remove('allpdffiles.zip')

		elif self.pdf_report == 'invoice':
			var = 0
			for active_ids in self.env['account.move'].browse(self._context.get('active_ids')):
				pdf = self.env.ref('account.account_invoices').render_qweb_pdf(active_ids.id)[0]
				list1.append(active_ids)
				if active_ids.name == '/':
					var += 1
					with open('/tmp/' +(active_ids.name).replace('/','_') + "%s.pdf" % (var), "wb") as outfile:
						outfile.write(pdf)
				else:
					with open('/tmp/' +(active_ids.name).replace('/','_') + ".pdf", "wb") as outfile:
						outfile.write(pdf)

			with ZipFile('/tmp/allpdffiles.zip', 'w') as myzip:
				var2 = 0
				for order in list1:
					if order.name == '/':
						var2 += 1
						myzip.write('/tmp/' +(order.name).replace('/','_') + "%s.pdf" % (var2))
					else:
						myzip.write('/tmp/' +(order.name).replace('/','_') + ".pdf")

			with open("/tmp/allpdffiles.zip", "rb") as f:
				converts = f.read()
				encoded = base64.b64encode(converts)

			self.file_name = 'Invoices.zip'	
			self.download_pdf_report = encoded

			var3 = 0
			for result in list1:
				if result.name == '/':
					var3 += 1
					os.remove('/tmp/' +(result.name).replace('/','_') + "%s.pdf" % (var3))
				else:
					os.remove('/tmp/' +(result.name).replace('/','_') + ".pdf")
			os.remove('/tmp/allpdffiles.zip')

		self.write({'state':'done'})

		return {
			'name':'Download Multiple Separate Invoices',
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'wizard.download.pdf',
			'res_id': self.id,
			'target': 'new',
		}


	def wizard_download(self):
		return {'type': 'ir.actions.act_window_close'}
