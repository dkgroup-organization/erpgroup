# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import os
import logging
import unicodedata
import tempfile
import time
import csv
from . import format_cegid
import zipfile

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


def format_amount(amount, length):
    """ return text with no point with a fixed lenght """
    c1 = ("%0.2f" % amount).replace('.', '')
    if len(c1) <= length:
        c2 = ' ' * (length - len(c1)) + c1
    else:
        # there is a problem
        msg = "This amount is to big: %0.2f\n%s" % (amount, length)
        raise ValidationError(msg)
    return c2





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
                ('date', '>=', '2022-01-01'),
                ('company_id', '=', self.company_id.id),
                ('state', 'not in', ['cancel', 'draft'])
            ]
            move_ids = self.env['account.move'].search(condition, order="date")
            if move_ids:
                self.date_from = move_ids[0].date
                self.date_to = move_ids[-1].date
                self.message = ''
            else:
                self.date_from = False
                self.date_to = False
                self.message = ''
        else:
            self.date_from = False
            self.date_to = False
            self.message = ''

    @api.model
    def get_cegid_format_m(self):
        """ read file with the definition of CEGID format
        return dictionnnary with : name of field: (start position int, width int, value text)
        The CSV file column are : code;position;width;default;description"""
        res = {}
        config = format_cegid.CEGID_FORMAT_M.split('\n')

        for raw in config:
            raw = raw.split(';')
            res[raw[0]] = {'start': int(raw[1]) - 1,
                           'width': int(raw[2]),
                           'end': int(raw[1]) - 1 + int(raw[2]),
                           'default': raw[3],
                           }
        return res

    def button_export_line(self):
        "export the account move line"

        for wizard in self:



            def format_data_line(data_line, conf_line):
                """ return a CEGID formated line"""
                data_line_text = ' ' * format_cegid.CEGID_LINE_LENGTH
                for field_name in list(data_line.keys()):
                    if len(data_line[field_name]) != conf_line[field_name]['width']:
                        raise ValidationError('The length of this value %s is not ok:\n>>>%s<<< ' % (
                            field_name, data_line[field_name]))
                    start = conf_line[field_name]['start']
                    end = conf_line[field_name]['end']
                    data_line_text = data_line_text[0:start] + data_line[field_name] + data_line_text[end:]
                return data_line_text

            def format_libelle(line, length):
                """ format libelle """
                move_name = ' ' + txt_cleanup(line.move_id.name)
                partner_name = txt_cleanup(line.move_id.partner_id.name)

                for search_txt in ['-DKPRINTING', '-DKDIGITAL', '-DKFACTORY', '-DKINDUSTRIE']:
                    if search_txt in move_name:
                        move_name = move_name.replace(search_txt, '')

                if len(move_name) > length:
                    text = move_name[:length]
                else:
                    partner_len_max = length - len(move_name)
                    if len(partner_name) > partner_len_max:
                        partner_name = partner_name[:partner_len_max]

                    text = partner_name + ' ' * (length - len(move_name) - len(partner_name)) + move_name
                return text

            # Check the partner configuration
            partner_ko_ids = self.env['res.partner']
            msg = "This partner are not correctly configured:\n"

            # List the move to export
            condition = [
                ('date', '>=', wizard.date_from),
                ('date', '<=', wizard.date_to),
                ('journal_id.type', '=', wizard.journal_type),
                ('company_id', '=', wizard.company_id.id),
                ('export_id', '=', False),
                ('state', 'not in', ['cancel', 'draft'])
            ]
            move_ids = self.env['account.move'].search(condition)
            datas = []
            conf_line = self.get_cegid_format_m()

            # Prepare attachment
            temp_dir = tempfile.TemporaryDirectory()

            # Start extract line
            for move in move_ids:

                default_data_line = {}

                #Check if invoice pdf
                if move.is_invoice(include_receipts=True):
                    pdf = self.env.ref('account.account_invoices').sudo().render_qweb_pdf(move.ids)
                    # The pdf name is limite to 8 character in CEGID, so this name is ok
                    pdf_name = "F%07i" % move.id
                    path_name = os.path.join(temp_dir.name, pdf_name + '.pdf')
                    pdf_file = open(path_name, 'wb')
                    pdf_file.write(pdf[0])
                    pdf_file.close()
                    default_data_line['piece8'] = pdf_name
                    default_data_line['piece_jointe'] = pdf_name + '.pdf'

                for line in move.sudo().line_ids:

                    data_line = default_data_line.copy()
                    data_line['type'] = 'M'

                    # compte tiers
                    if line.compte_tiers and line.compte_tiers[0] == '?':
                        partner_ko_ids |= line.move_id.partner_id
                    elif line.compte_tiers:
                        add_blanck = conf_line['compte']['width'] - len(line.compte_tiers)
                        if add_blanck < 0:
                            add_blanck = 0

                        data_line['compte'] = line.compte_tiers + ' ' * add_blanck
                    else:
                        data_line['compte'] = line.compte_tiers or line.account_id.export_code


                    if partner_ko_ids:
                        continue

                    data_line['journal2'] = line.journal_id.export_code2
                    data_line['journal3'] = line.journal_id.export_code3
                    data_line['folio'] = '000'
                    data_line['code_libelle'] = 'F'
                    data_line['date'] = line.move_id.invoice_date.strftime("%d%m%y") \
                                        or line.move_id.date.strftime("%d%m%y")
                    if line.debit > line.credit:
                        data_line['sens'] = 'D'
                        data_line['montant'] = format_amount(line.debit, conf_line['montant']['width'])
                    else:
                        data_line['sens'] = 'C'
                        data_line['montant'] = format_amount(line.credit, conf_line['montant']['width'])

                    data_line['Libelle'] = format_libelle(line, conf_line['Libelle']['width'])
                    data_line['piece10'] = "%010i" % line.move_id.id

                    if line.date_maturity:
                        data_line['date_echeance'] = line.date_maturity.strftime("%d%m%y")

                    datas.append(format_data_line(data_line, conf_line))

            if partner_ko_ids:
                for partner_ko in partner_ko_ids:
                    msg += "%s\n" % partner_ko.name
                raise ValidationError(msg)


            #extract data
            content = ''
            for line in datas:
                content += line + '\n'

            wizard.content = content or ''

            # Create ZIP file with pdf
            file_name_txt = 'export_%s_%s.txt' % (fields.Date.today(), wizard.journal_type)
            path_name = os.path.join(temp_dir.name, file_name_txt)
            file_txt = open(path_name, 'w')
            file_txt.write(wizard.content)
            file_txt.close()

            # write files and folders to a zipfile
            zip_filename = tempfile.gettempdir() + '/export_%s_%s.zip' % (wizard.id, fields.Datetime.now().strftime('%Y%m%d_%H%M%S'))
            zip_file = zipfile.ZipFile(zip_filename, 'w')
            with zip_file:
                # write each file seperately
                for root, dirs, files in os.walk(temp_dir.name):
                    for file in files:
                        zip_file.write(os.path.join(root, file), file)
            zip_file.close()

            # Attachment csv
            attachment_vals = {}
            zip_file = open(zip_filename, 'rb')
            attachment_vals['name'] = zip_filename
            attachment_vals['datas'] = base64.encodebytes(zip_file.read())
            zip_file.close()

            attachment_vals['mimetype'] = "application/zip"
            attachment_vals['description'] = "Export comptable CEGID"
            attachment_vals['res_model'] = 'account.export.history'
            attachment = self.env['ir.attachment'].create(attachment_vals)

            # change temporary name
            attachment.name = 'export_%s_%s_%s.zip' % (
                fields.Date.today(),
                wizard.journal_type,
                attachment.id)
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
