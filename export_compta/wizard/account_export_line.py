# -*- coding: utf-8 -*-

from odoo import fields, models, api
import base64
import logging
import unicodedata

_logger = logging.getLogger(__name__)


def remove_accents(input_str):
    only_ascii = unicodedata.normalize('NFD', input_str).encode('ascii', 'ignore')
    if type(only_ascii) == bytes:
        return only_ascii.decode()
    else:
        return only_ascii


def txt_cleanup(text):
    if text:
        text = remove_accents(text)
        text = text.replace('\"', ' ')
        text = text.replace('\n', ' ')
        text = text.replace(';', ' ')
        text = text.replace('%', ' ')
        text = text.replace('"', ' ')
        text = text.replace('   ', ' ')
        text = text.replace('  ', ' ')
        text = text.replace('  ', ' ')
        text = text.strip()
        return text
    else:
        return ''


class AccountExportMoveLine(models.TransientModel):
    _name = 'account.export.moveline'
    _description = 'Export move line.'

    journal_type = fields.Selection([
            ('sale', 'Sales'),
            ('purchase', 'Purchase'),
            ('bank', 'Bank'),
            ('cash', 'Cash'),
            ('general', 'Divers')], string="Journal type", required=True)

    date_from = fields.Date('Start Date', required=True)
    date_to = fields.Date('End Date', required=True)
    message = fields.Html('Message', readonly=True)
    content = fields.Text('Content')

    attachment_id = fields.Many2one('ir.attachment', string='File', readonly=True)
    attachment_name = fields.Char(related='attachment_id.name', readonly=True)
    attachment_datas = fields.Binary(related='attachment_id.datas', readonly=True)
    company_id = fields.Many2one('res.company', string='Company')

    @api.model
    def default_get(self, fields):
        "return default value"
        res = super(AccountExportMoveLine, self).default_get(fields)
        res['company_id'] = self.env.company.id
        return res

    @api.onchange('journal_type')
    def onchange_journal(self):
        "check last date change"
        if self.journal_type:

            condition = [
                    ('journal_id.type', '=', self.journal_type),
                    ('export_id', '=', False),
                    ('date', '>=', '2018-01-01'),
                    ('company_id', '=', self.company_id.id),
                    ('state', 'not in', ['cancel', 'draft'])
                    ]
            move_ids = self.env['account.move'].search(condition, order="date")
            if move_ids:
                self.date_from = move_ids[0].date
                self.date_to = move_ids[-1].date
                # self.message = "%s pieces" % len(move_ids)
            else:
                self.date_from = False
                self.date_to = False
                self.message = ''
        else:
            self.date_from = False
            self.date_to = False
            self.message = ''


    def button_export_line(self):
        "export the account move line"

        for wizard in self:

            condition = [
                ('date', '>=', wizard.date_from),
                ('date', '<=', wizard.date_to),
                ('journal_id.type', '=', wizard.journal_type),
                ('company_id', '=', wizard.company_id.id),
                ('export_id', '=', False),
                ('state', 'not in', ['cancel', 'draft'])
                ]
            move_ids = self.env['account.move'].search(condition)

            column_template = ['JOURNAL', 'REF_PIECE', 'DATE_PIECE', 'LIB_PIECE', 'COMPTE', 'CPTE_GENERAL',
                        'CPTE_TIERS', 'TIERS', 'LIBELLE', 'DEBIT', 'CREDIT', 'DEV']

            datas = []

            # TODO: before export check all CPT_TIER, list the partner without compte tiers and raise user with the list

            # Start extract line
            for move in move_ids:
                for line in move.sudo().line_ids:

                    data_line = {}

                    data_line['JOURNAL'] = line.journal_id.code
                    data_line['DATE_PIECE'] = move.invoice_date or move.date or ''
                    data_line['REF_PIECE'] = move.ref or move.name or ''
                    data_line['LIB_PIECE'] = move.name or move.ref or ''
                    data_line['CPTE_GENERAL'] = line.account_id.code or ''
                    data_line['CPTE_TIERS'] = line.compte_tiers or ''
                    data_line['COMPTE'] = data_line['CPTE_TIERS'] or data_line['CPTE_GENERAL']
                    data_line['TIERS'] = line.partner_id.name or ''
                    data_line['LIBELLE'] = line.name or ''
                    data_line['DEBIT'] = line.debit
                    data_line['CREDIT'] = line.credit
                    data_line['DEV'] = 'EUR'

                    # Unicode, pas d'accent
                    for key in ['LIBELLE', 'REF_PIECE', 'LIB_PIECE']:
                        data_line[key] = txt_cleanup(data_line[key])

                    # Float with coma not point
                    for key in ['DEBIT', 'CREDIT']:
                        value = "%s" % (data_line[key])
                        data_line[key] = value.replace('.', ',')

                    datas.append(data_line)

            content = ''
            for column in column_template:
                if content:
                    content += ';'
                content += column
            content += '\n'

            for data_line in datas:
                line_text = ''
                for column in column_template:
                    if line_text:
                        line_text += ';'
                    if column in list(data_line.keys()):
                        line_text += "%s" % (data_line[column])
                line_text.replace('\r\n', ' ').replace('\n', ' ')
                content += line_text + '\n'

            wizard.content = content or ''

            # Attachment csv
            attachment_vals = {}
            attachment_vals['datas'] = base64.encodestring(
                            wizard.content.encode('utf-8'))
            attachment_vals['mimetype'] = "text/csv"
            attachment_vals['description'] = "Export comptable CEGID"
            attachment_vals['name'] = "wizard_%s.csv" % (wizard.id)
            attachment_vals['res_model'] = 'account.export.history'
            attachment = self.env['ir.attachment'].create(attachment_vals)

            file_name = 'export_%s_%s_%s.csv' % (
                            fields.Date.today(),
                            wizard.journal_type,
                            attachment.id)
            attachment.name = file_name
            wizard.attachment_id = attachment

            # History export
            history_vals = {'date': fields.Date.today()}
            history_vals['name'] = "du %s au %s: %s pieces %s" % (
                            wizard.date_from, wizard.date_to,
                            len(move_ids), wizard.journal_type)
            history_vals['attachment_id'] = attachment.id
            history_vals['company_id'] = wizard.company_id.id

            history = self.env['account.export.history'].create(history_vals)

            # Complete info
            attachment.res_id = history.id
            move_ids.write({'export_id': history.id})
            wizard.message = history_vals['name']
