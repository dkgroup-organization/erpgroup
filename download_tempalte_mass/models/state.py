# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime
import base64



class MassMailing2(models.Model):
    
  _inherit = 'mailing.mailing'
  def download_template(self):
    f_read = open('test.html','w')
    message = self.body_arch
    f_read.write(message)
    file_data = f_read.read()
    values = {
            'name': "Name of text file.txt",
            'datas_fname': 'print_file_name.txt',
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': file_data.encode('utf8').encode('base64'),
        }
    attachment_id = self.env['ir.attachment'].sudo().create(values)
    #Prepare your download URL
    download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
    base_url = self.env['ir.config_parameter'].get_param('web.base.url')
    
    return {
        "type": "ir.actions.act_url",
        "url": str(base_url)  +  str(download_url),
        "target": "new",
     }







    body_arch
