# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class AccountExportHistory(models.Model):
    _name = 'account.export.history'
    _description = 'Export history'
    _order = "name asc"

    date = fields.Date('Date', required=True)
    name = fields.Char('Description', required=True)
    content = fields.Text('Message', readonly=True)
    attachment_id = fields.Many2one('ir.attachment', string="Attachment")
    attachment_name = fields.Char(related='attachment_id.name', readonly=True)
    attachment_datas = fields.Binary(related='attachment_id.datas', readonly=True)

    move_ids = fields.One2many('account.move', 'export_id', string='Account move')
    company_id = fields.Many2one('res.company', string='Company')
