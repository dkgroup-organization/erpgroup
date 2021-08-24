from odoo import api, fields, models, _

import pdfrw,os, tempfile, base64
import logging


_logger = logging.getLogger( __name__ )

# constantes
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

class ReportCertificate(models.TransientModel):
    _name = 'report.certificate'

    company_name = fields.Char("Nom d'entreprise")
    company_adress = fields.Char("Adresse d'entreprise")
    partner_id = fields.Many2one("res.partner","Client")
    client_name = fields.Char('Nom de client')
    client_adress = fields.Char("Adresse de client")
    manager_name = fields.Char("Nom de Maitre d'oeuvrage")
    manager_adress = fields.Char("Adresse de Maitre d'oeuvrage")
    controller_name = fields.Char("Nom de Controleur")
    controller_adress = fields.Char("Adresse de Controleur")
    site_name = fields.Char('Nom de chantier')
    site_adress = fields.Char('Adresse de chantier')
    date_start = fields.Date("Date début de chantier")
    date_end = fields.Date("Date fin de chantier")
    description = fields.Text("Description technique")
    amount= fields.Float("Montant HT du marché")
    description_amount = fields.Text("Objet et montant HT")
    date_without = fields.Date("Date sans reserve")
    date_with = fields.Date("Date avec reserve")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
    )

    @api.onchange('company_id')
    def _update_company(self):
        self.company_name=self.company_id.name
        self.company_adress = self.company_id.street

    @api.onchange('partner_id')
    def _update_partner(self):
        self.client_name = self.partner_id.name
        self.client_adress =  self.partner_id.street
        self.manager_name = self.partner_id.project_manager.name
        self.manager_adress = self.partner_id.project_manager.street
        self.controller_name = self.partner_id.technical_controller.name
        self.controller_adress = self.partner_id.technical_controller.street


    def fill_pdf(self, input_pdf_path, output_pdf_path, data_dict):
        template_pdf = pdfrw.PdfReader(input_pdf_path)
        for page in template_pdf.pages:
            annotations = page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if key in data_dict.keys():
                            if type(data_dict[key]) == bool:
                                if data_dict[key] == True:
                                    annotation.update(pdfrw.PdfDict(
                                        AS=pdfrw.PdfName('Yes')))
                            else:
                                annotation.update(
                                    pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                                )
                                annotation.update(pdfrw.PdfDict(AP=''))
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

    def _prepare_data(self,url_file,data):
        dossier = os.path.dirname(__file__)
        attestation = dossier + url_file
        f, filename = tempfile.mkstemp()
        self.fill_pdf(attestation, filename,data)
        order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        attachment_id = self.create_attachment_from_pdf(attestation.split("/")[-1], filename, order.id)
        order.piece_joint = [(4, attachment_id.id)]
        return {
            'type': 'ir.actions.act_url',
            "url": attachment_id.local_url,
            'target': 'new',
        }




    def print_verbal(self):
        url = "/../static/src/documents/Batiavenir_Proces_Verbal_Reception.pdf"
        data_verbal = {
            'Nom_Entreprise': self.company_name,
            'Adresse_Entreprise': self.company_adress,
            # 'Adresse_Entreprise 5': self.description,
            # 'Nom_Entreprise 5': self.date_end,
            # 'Nom_Entreprise 6': self.date_start,
            # 'Nom_Entreprise 7': self.amount,
            # 'Adresse_Entreprise 6': self.description_amount,
            # 'Nom_Entreprise 1': self.client_name,
            # 'Adresse_Entreprise 1': self.client_adress,
            # 'Nom_Entreprise 2': self.manager_name,
            # 'Adresse_Entreprise 2': self.manager_adress,
            # 'Nom_Entreprise 3': self.controller_name,
            # 'Adresse_Entreprise 3': self.controller_adress,
            # 'Nom_Entreprise 4': self.site_name,
            # 'Adresse_Entreprise 4': self.site_adress,
        }
        attachment = self._prepare_data(url,data_verbal)
        return attachment

    def print_work(self):
        url= "/../static/src/documents/Batiavenir_Attestation_Travaux.pdf"
        data_attestation = {
            'Nom_Entreprise': self.company_name,
            'Adresse_Entreprise': self.company_adress,
            'Adresse_Entreprise 5': self.description,
            'Nom_Entreprise 5': self.date_end,
            'Nom_Entreprise 6': self.date_start,
            'Nom_Entreprise 7': self.amount,
            'Adresse_Entreprise 6': self.description_amount,
            'Nom_Entreprise 1': self.client_name,
            'Adresse_Entreprise 1': self.client_adress,
            'Nom_Entreprise 2': self.manager_name,
            'Adresse_Entreprise 2': self.manager_adress,
            'Nom_Entreprise 3': self.controller_name,
            'Adresse_Entreprise 3': self.controller_adress,
            'Nom_Entreprise 4': self.site_name,
            'Adresse_Entreprise 4': self.site_adress,
        }
        attachment = self._prepare_data(url,data_attestation)
        return attachment




    def create_attachment_from_pdf(self, name, file, id):
        c = open(file, "rb+").read()

        return self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            'datas': base64.encodestring(c),

        })

