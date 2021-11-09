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
    import base64
    donnee = self.body_arch if self.body_arch else "<html></html>"
    # output is where you have the content of your file, it can be
    # any type of contentoutput
    # encode
    result = base64.b64encode(bytes(donnee, 'utf-8') or b'')
    # get base url
    base_url = self.env['ir.config_parameter'].get_param('web.base.url')
    attachment_obj = self.env['ir.attachment']
    # create attachment
    attachment_id = attachment_obj.create(
        {'name': "name", 'res_name': self.name +'.html', 'datas': result, 'name' : self.name +'.html'})
    # prepare download url
    download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
    # download
    return {
        "type": "ir.actions.act_url",
        "url": str(base_url) + str(download_url),
        "target": "new",
    }
