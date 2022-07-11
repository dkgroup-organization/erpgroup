# -*- coding: utf-8 -*-

import base64
import math
import pytz
import tempfile
import codecs
import datetime
import csv

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

log = logging.getLogger(__name__).info
_logger = logging.getLogger(__name__)

FORMAT_ENCODING = [('utf-8', 'utf-8'), ('windows-1252', 'windows-1252'), ('latin1', 'latin1'),
    ('latin2', 'latin2'), ('utf-16', 'utf-16'), ('windows-1251', 'windows-1251')]
FORMAT_SEPARATOR = [(';', 'Semicolon'), (',', 'Comma'), ('\t', 'Tab')]
FORMAT_DATE = [('ddmmyy', 'ddmmyy'), ('dd/mm/yyyy', 'dd/mm/yyyy'), ('yyyy-mm-dd', 'yyyy-mm-dd'),
    ('yyyymmdd', 'yyyymmdd'), ('mm/dd/yyyy', 'mm/dd/yyyy')]
MAP_MONTH_NAME = {'janv': '01', u'f\xe9vr': '02', 'mars': '03', 'avr': '04', 'mai': '05',
        'juin': '06', 'juil': '07', u'ao\xfbt': '08', 'sept': '09', 'oct': '10',
        'nov': '11', u'd\xe9c': '12'}

MIN_COLUMN = 2
FLOAT_PRECISION = 0.01
TIMEZONE = "Europe/Paris"


def to_float(text_number):
    "always return float, if error return 0.0"
    try:
        res = float(str(text_number).replace(' ', '').replace(',', '.').replace('%', '')) or 0.0
    except:
        res = 0.0
    return res


def quotechar(text, quotechar='"'):
    "return text without quotechar"
    if len(text) >= 2:
        if text[0] == quotechar and text[-1] == quotechar:
            return text[1:-1]
        else:
            return text
    else:
        if text:
            return text
        else:
            return ''


def to_bool(text):
    "return bool"
    text = text.strip().lower() or '?'
    if text in ["yes", "oui", "1"]:
        return True
    else:
        return False


class ImportData(models.TransientModel):
    _name = "import.data"
    _description = "CSV file import"

    name = fields.Char('Name')
    import_date = fields.Datetime('Date of the import')
    import_date_todo = fields.Boolean("Import date todo")
    filename = fields.Char('File Name')
    check_field = fields.Char('Reference field')

    file_binary = fields.Binary('Import File', required=True)

    data = fields.Binary('Data')
    configuration = fields.Text("configuration")
    type_import = fields.Char("Type")
    type_import_html = fields.Html("Description")
    preview = fields.Text(string='Preview', help="Content of the file", readonly=True, default='')
    content = fields.Text(string='content', help="Content of the file", readonly=True, default='')

    encoding = fields.Selection(FORMAT_ENCODING, 'Encoding')
    delimiter = fields.Selection(FORMAT_SEPARATOR, string="Delimiter")
    quotechar = fields.Char('Quotechar')
    header = fields.Integer('Header', help='First row contains the label of the column, pass some lines before start')
    date = fields.Selection(FORMAT_DATE, string="Date")
    decimal = fields.Selection([(',', 'comma'), ('.', 'point')], string="Decimale")
    error = fields.Text('Import error', readonly=True)
    model_id = fields.Many2one('ir.model', 'Model object')
    active_id = fields.Integer('Active id')
    example_file = fields.Char("Example file")

    def button_import(self):
        "import the data"
        for wizard in self:
            wizard.error = ''
            if wizard.model_id.model == "res.partner" and wizard.type_import == 'COMPTE TIERS':
                wizard.import_partner_account_ref()



    @api.model
    def default_get(self, fields):
        "default value"
        res = super().default_get(fields)

        default = {
            'encoding': 'utf-8',
            'delimiter': ';',
            'quotechar': '"',
            'header': 0,
            'date': 'yyyy-mm-dd',
            'decimal': '.',
            }
        optional = ['import_date_todo', 'type_import', 'configuration']

        context = dict(self._context or {})
        for key_name in list(default.keys()) + optional:
            if context.get(key_name):
                default[key_name] = context.get(key_name)

        model_name = context.get("model_name")
        if model_name:
            model_ids = self.env['ir.model'].search([('model', '=', model_name)])
            if model_ids:
                default['model_id'] = model_ids[0].id



        res.update(default)
        return res

    @api.onchange('encoding', 'header', 'check_field')
    def _onchange_configuration(self):
        "save the csv file on local disque"
        if self.file_binary:
            self._onchange_file()

    @api.onchange('file_binary')
    def _onchange_file(self):
        "save the csv file on local disque"
        if self.file_binary:

            #Save data on disk
            if not self.filename:
                #temp_dir = tempfile.TemporaryDirectory()
                file_name = tempfile.mkstemp('.in.csv', 'odoo-', '/tmp')[1]
                csvfile = open(file_name, 'wb')
                csvfile.write(base64.b64decode(self.file_binary))
                csvfile.close()
                self.filename = file_name
            else:
                file_name = self.filename

            content = ''
            #Detect encoding by test, use the encoding defined in first test
            if self.encoding and (self.encoding, self.encoding) != FORMAT_ENCODING[0]:
                list_encoding = [(self.encoding, self.encoding)] + FORMAT_ENCODING
            else:
                list_encoding = FORMAT_ENCODING

            for encoding_format in list_encoding:
                try:
                    csvfilein = open(file_name, 'r', encoding=encoding_format[0])
                    content = csvfilein.read()
                    csvfilein.close()
                    self.encoding = encoding_format[0]
                except:
                    self.encoding = False

                if self.encoding:
                    break

            #load data
            if self.encoding and content:
                data = content.split('\n')

                #detect the first row by the name of column: check_field
                if self.check_field:
                    self.header = 0
                    for line in data:
                        if self.check_field in line:
                            break
                        else:
                            self.header += 1

                        if self.header > 50:
                            raise UserError(_('There is an error when loading the header of the file, The field <%s> is not finding.' % (self.check_field)))

                #load data
                if self.header and len(data) > self.header:
                    data = data[self.header:]

                if len(data) < 1:
                    raise UserError(_('There is no data.'))

                header = data[0]
                #detect delimiter
                if self.delimiter in header:
                    pass
                elif ';' in header:
                    self.delimiter = ';'
                elif ',' in header:
                    self.delimiter = ','
                elif '\t' in header:
                    self.delimiter = '\t'
                else:
                    raise UserError(_('There is an error when loading the header of the file, check the delimiter configuration.'))

                #save the csv in file
                file_name_out = file_name.replace('.in.csv', '.out.csv')
                csvfileout = open(file_name_out, 'w', encoding=self.encoding)
                for row in data:
                    csvfileout.write(row + '\n')
                csvfileout.close()
                self.filename = file_name_out

                #load csv data
                csv_data = self.load_data()[self.id]

                if len(header.split(self.delimiter)) > 15:
                    # preview text
                    nb_line = 0
                    html_preview = ""
                    for line in data:
                        html_preview += line + '%s<br/>'
                        self.preview = html_preview
                        nb_line += 1
                        if nb_line > 10:
                            break
                else:
                    #preview html
                    html_preview = ""
                    html_preview += "<thead><tr>"
                    csv_header = []
                    for csv_field in header.split(self.delimiter):
                        csv_field = quotechar(csv_field, quotechar=self.quotechar)
                        html_preview += '<td>%s</td>' % (csv_field)
                        csv_header.append(csv_field.strip())
                    html_preview += "</tr></thead>"

                    nb_line = 0
                    for line in csv_data:
                        html_preview += "<tr>"
                        for csv_field in csv_header:
                            if csv_field in list(line.keys()):
                                html_preview += "<td>%s</td>" % (line[csv_field])
                            else:
                                html_preview += "<td></td>"
                        html_preview += "</tr>"
                        nb_line += 1
                        if nb_line > 10:
                            break

                    self.preview = '<table class="o_list_view table table-condensed table-bordered">' + html_preview + "</table>"
            else:
                raise UserError(_('There is an error when loading the file, check the encoding character configuration.'))
        else:
            self.filename = ''
            self.preview = ''

    def load_data(self, lower=False):
        "Load data in a list of dictionnary"
        res = {}
        # Start
        for wizard in self:
            res[wizard.id] = []

            with open(wizard.filename, encoding=wizard.encoding) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=wizard.delimiter, quotechar=wizard.quotechar)

                data = []
                header = []
                for row in spamreader:
                    if row:
                        line = {}
                        if not header:
                            for csv_field in row:
                                if lower:
                                    header.append(csv_field.strip().lower())
                                else:
                                    header.append(csv_field.strip())
                        else:
                            for i, csv_field in enumerate(header):
                                line[csv_field] = row[i].strip()
                            data.append(line)
                res[wizard.id] = data
        return res

    @api.model
    def get_map_country(self, data):
        """ Return country"""
        map_country = {'France': 75}
        for wizard in self:
            for data_line in data:
                code = data_line.get('pays')
                if code and code not in list(map_country.keys()):
                    country_ids = self.env['res.country'].search([('code', '=', code)])
                    if country_ids:
                        map_country[code] = country_ids[0].id
        return map_country

    @api.model
    def get_partner(self, parent, data_line, map_country):
        """ Return country"""
        d_vals = {
            'type': 'delivery',
            'parent_id': parent and parent.id or False,
            'name': data_line.get('nom', '?') + ' ' + data_line.get('prenom', '?'),
            'street': data_line.get('street'),
            'street2': data_line.get('street2'),
            'street3': data_line.get('street3'),
            'street4': data_line.get('street4'),

            'email': data_line.get('email'),
            'phone': data_line.get('telephone'),
            'zip': data_line.get('code_postal'),
            'city': data_line.get('ville'),
            'country_id': map_country[data_line.get('pays', 'France')],
        }
        condition = ['&', ('parent_id', '=', d_vals['parent_id']), '|',
                     '&', ('email', '=', d_vals['email']), ('name', '=', d_vals['zip']),
                     '&', ('email', '=', d_vals['email']), ('city', '=', d_vals['city'])
                     ]
        res_destination_ids = self.env['res.partner'].search(condition)
        if res_destination_ids:
            res_destination = res_destination_ids[0]
        else:
            res_destination = self.env['res.partner'].create(d_vals)

        return res_destination


    def import_partner_account_ref(self):
        "start import"
        load_data = self.load_data()
        # Start
        for wizard in self:
            nb_line = 1
            nb_ok = 0
            data = load_data[wizard.id]

            for data_line in data:
                # Load data_line
                nb_line += 1
                name = data_line.get('Intitulé', '')
                if not name:
                    continue
                condition = [('name', 'ilike', '%' + name + '%'), ('invoice_ids', '!=', False)]
                partner_ids = self.env['res.partner'].search(condition)
                if partner_ids:
                    nb_ok += 1
                    for partner in partner_ids:
                        if data_line.get('Type', '') == 'C':
                            partner.third_account_customer = data_line.get('Numero', '')
                        elif data_line.get('Type', '') == 'F':
                            partner.third_account_supplier = data_line.get('Numero', '')
                        if not partner.ref:
                            partner.ref = data_line.get('Clé', '')
