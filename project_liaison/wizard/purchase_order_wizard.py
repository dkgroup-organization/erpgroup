# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

import logging,pprint
import pdfrw,os, tempfile, base64

_logger = logging.getLogger( __name__ )

# constantes
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


class accountMoveLineBouton(models.Model):
    _inherit = 'account.move.line'

    def xdupliquer_ligne(self):
        return self.with_context({"check_move_validity": False}).copy()

class jointpieceLiaison(models.Model):
    _inherit = 'account.move'

    pv_livraison_30k_prime = fields.Many2many( "ir.attachment", "livraison_rel", "account_move_id",  "ir_attachment_id" ,"PV de livraison", domain=[("mimetype",   '=', "application/pdf")])
    bon_commande_30k_prime = fields.Many2many( "ir.attachment", "ref_bon_commande_30k_prime" ,  "account_move_id",  "ir_attachment_id", string="Bon de commande",domain=[("mimetype",   '=', "application/pdf")])
    accord_mail_30k_prime = fields.Many2many( "ir.attachment", "ref_accord_mail_30k_primee" , "account_move_id",  "ir_attachment_id" , string="Accord Mail",domain=[("mimetype",   '=', "application/pdf")])


    def button_draft(self):
        x = super(jointpieceLiaison, self).button_draft()
        self.invoice_payment_term_id = self.partner_id.property_supplier_payment_term_id


    @api.onchange('piece_joint',)
    def _pdf_constraint(self):
        for element in self.piece_joint:
            if element.name.split(".")[-1].lower() !="pdf" and "virtual_" in str(element.id):
                raise ValidationError("seul les fichiers PDF sont permis")


    def action_post(self):
        sortie = ""
        if self.amount_total >= 30000 and self.type == "out_invoice":
            if not self.pv_livraison_30k_prime:
                sortie += "PV de livraison\n"

            if not self.bon_commande_30k_prime:
                sortie += "Bon de commande\n"

            if not self.accord_mail_30k_prime:
                sortie += "Accord mail."
        if sortie:
            message = "Pour les factures de plus de 30.000, veuillez ajouter ces documents:\n"
            raise ValidationError(message + sortie)

        #partie 20%
        taux = 20
        error_msg = "Un taux de 20% est requis pour les particuliers"
        if 0 : #self.partner_id.company_type == 'person':
            for line in self.invoice_line_ids:
                flag = False
                if not line.tax_ids:
                    raise ValidationError(error_msg)
                for tax in line.tax_ids:
                    if tax.amount == taux:
                        flag = True
                        break
                if (not flag):
                    raise ValidationError(error_msg)
        x = super(jointpieceLiaison, self).action_post()


class Ajouter_achats_project(models.TransientModel):
		_name = 'ajouter.achats.projectt'
		_description = "Ajouter projet"

		achats = fields.Many2one('purchase.order', string='Achat', required = True,domain=lambda self:self._get_achats())


		def _get_achats(self):
			purchases_done = self.env['purchase.order'].search([("state", "=", "purchase"), ])
			return [('id', 'in', [purchase_done.id  for purchase_done in purchases_done if purchase_done.is_shipped ] )]

		def action_add_projet(self):
			data = self.env['project.project'].browse(self._context.get('active_ids',[]))
			data.achats = [(4, self.achats.id)]
			self.achats.projet = data.id



class IrAttachmentsHelper(models.Model):
    _inherit = 'ir.attachment'

    def ouvrir_facture(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'res_model': self.env.context["res_model"],
            'view_type': 'form',
            'domain': [('id', '=', self.env.context["res_id"])],
            'active_id': self.env.context["res_id"],
            'res_id': self.env.context["res_id"],
            'view_id': self.env.ref('account.view_move_form').id,
            'view_mode': 'form',
            'target': 'new',
            "mode": 'readonly',
        'flags':{"mode": 'readonly'},
        }


class projecto(models.Model):
    _inherit = 'project.project'

    def _default_documents_project(self):
        all_documents_ids = []

        for devis in self.devis:
            all_documents_ids += [attachment.id for attachment in devis.piece_joint]

        for fact in self.factures + self.factures_fournisseurs :
            all_documents_ids += [attachment.id for attachment in fact.piece_joint]
            all_documents_ids += [attachment.id for attachment in fact.pv_livraison_30k_prime]
            all_documents_ids += [attachment.id for attachment in fact.bon_commande_30k_prime]
            all_documents_ids += [attachment.id for attachment in fact.accord_mail_30k_prime]

        self.all_documents = all_documents_ids

    amount_untaxed_achats_associes_untaxed = fields.Monetary(string='Total HT des achats confirmés,  livrés et associé',
                                                     xstore=True,
                                                     readonly=True, compute='_amount_untaxed_achats_associes', tracking=True)

    amount_untaxed_achats_associest_total_achats = fields.Monetary(string='Total TTC des achats confirmés,  livrés et associé',
                                                     xstore=True,
                                                     readonly=True, compute='_amount_untaxed_achats_associes', tracking=True)

    amount_untaxed_achats = fields.Monetary(string='Total HT des achats livrés', xstore=True, readonly=True, compute='_amount_all22', tracking=True)
    amount_total_achats = fields.Monetary(string='Total TTC des Achats ', xstore=True, readonly=True, compute='_amount_all22')

    all_documents = fields.Many2many("ir.attachment",
        compute=_default_documents_project
    )

    devis = fields.Many2many(
        "sale.order", 'sale_order_move_rel1', string="Devis")
    achats = fields.Many2many(
        "purchase.order", 'sale_order_move_rel2', string="Achats", )
    factures = fields.Many2many(
        "account.move", 'sale_order_move_rel3', string="Factures", compute="_get_factures_clients")

    factures_fournisseurs = fields.Many2many(
        "account.move", 'sale_order_move_rel4', string="Factures Fournisseurs", compute="_get_factures_fournisseurs" )

    date_debut = fields.Datetime(string='Date de Demmarage Chantier', required=False, copy=False,
                                 default=fields.Datetime.now)
    date_fin = fields.Datetime(string='Date de fin de chanier',
                               required=False, copy=False, default=fields.Datetime.now)
    reference_chantier = fields.Char(string="Reference chantier")

    state = fields.Selection([('draft', 'Projet Valide'),('prod', 'Production'),('fact', 'Facturation'),('done', 'Terminé'),('cancel', 'Annuler'),], default='draft')

    articles_rep =  fields.Html(string = "Articles", compute="_get_articles")


    list_article_achat = fields.Many2many('purchase.order.line','project_project_purchase_order_line_rel',string="Liste des articles",compute="_get_article_achat")
    list_article_devis = fields.Many2many('sale.order.line','project_project_sale_order_line_rel',string="Liste des articles",compute="_get_article_devis")
    list_article_facture = fields.Many2many('account.move.line','project_project_account_move_line_rel',string="Liste des articles",compute="_get_article_facture")

    @api.depends('devis')
    def _get_article_devis(self):
        for rec in self:
            list = rec.devis.mapped('order_line').ids
            #            list+=rec.factures.mapped('invoice_line_ids').mapped('product_id').ids
            #            raise ValidationError(type(list))
            rec.list_article_devis = [(6, 0, list)]
        return True


    @api.depends('factures', 'factures_fournisseurs')
    def _get_article_facture(self):
        for rec in self:
            list = rec.factures_fournisseurs.mapped('invoice_line_ids').ids
            list += rec.factures.mapped('invoice_line_ids').ids
            rec.list_article_facture = [(6, 0, list)]
        return True

    @api.depends('achats')
    def _get_article_achat(self):
        for rec in self:
            list = rec.achats.mapped('order_line').ids
            rec.list_article_achat=[(6, 0, list)]
        return True








    def _get_factures_fournisseurs(self):
        for rec in self:
            invoices_ids = self.env['account.move'].search([('projet', '=', rec.id),('type', '=', 'in_invoice')]).ids
            rec.factures_fournisseurs = [(6, 0, invoices_ids)]
        return True


    def _get_factures_clients(self):
        for rec in self:
            invoices_ids = self.env['account.move'].search([('projet', '=', rec.id),('type', '=', 'out_invoice')]).ids
            rec.factures = [(6, 0, invoices_ids)]
        return True

    @api.depends('achats')
    def _amount_all22(self):
        for project in self:
            amount_untaxed = amount_total = 0.0
            for line in project.achats:
                if line.is_shipped:
                    amount_untaxed += line.amount_untaxed
                    amount_total += line.amount_total
            project.update({
                'amount_untaxed_achats': amount_untaxed,
                'amount_total_achats': amount_total,
            })


    @api.depends('achats')
    def _amount_untaxed_achats_associes(self):
        for project in self:
            amount_untaxed = amount_total = 0.0
            for line in project.achats:
                if  line.invoice_ids and line.is_shipped:
                    amount_untaxed += line.amount_untaxed
                    amount_total += line.amount_total
            project.update({
                'amount_untaxed_achats_associes_untaxed': amount_untaxed,
                'amount_untaxed_achats_associest_total_achats': amount_total,
            })

    def _get_articles(self):
        header = """<table class="editorDemoTable"  border="1">
<tbody>
<tr>
<td><strong>Article</strong></td>
<td><strong>Quantit&eacute;</strong></td>
<td><strong>Description</strong></td>
<td><strong>Fournisseur</strong></td>
</tr>"""
        body_temp  = f"""
<tr>
<td>%(name)s</td>
<td>%(quantite)s</td>
<td>%(description)s</td>
<td>%(fournisseur)s</td>
</tr>"""
        footer = """
</tbody>
</table>"""
        dico = {}


        for achat in self.achats:
            for line in achat.order_line:
                entree = dico.get(line.product_id.id, {"id":line.product_template_id.id, "name" :line.product_template_id.name, "quantite": 0, "description" : line.name if line.name else "", "fournisseur" : line.product_id.seller_ids[0].name.name if line.product_id.seller_ids else ""})
                dico[line.product_id.id] = entree
                dico[line.product_id.id]["quantite"] += line.product_qty

        out = header
        for k,v in dico.items():
            out += body_temp % v
        out += footer
        self.articles_rep = out


    def prod(self):
        self.write({
            'state': 'prod',
        })

    def fact(self):
        self.write({
            'state': 'fact',
        })

    def done(self):
        self.write({
            'state': 'done',
        })

    def cancel(self):
        self.write({
            'state': 'cancel',
        })

    def draft(self):
        self.write({
            'state': 'draft',
        })


class projectt(models.Model):
    _inherit = 'sale.order'

    projet = fields.Many2one('project.project', "Projet",
	                         help="Reference to Project")

    all_documents =  fields.Many2many("ir.attachment",
                                      compute="_get_all_documents"
    )


    def script_perso(self):
        sales = self.env["sale.order"].search([('projet','!=',False)])
        purchases = self.env["purchase.order"].search([('projet','!=',False)])
        factures = self.env["account.move"].search([('projet','!=',False)])
        sales2 = self.env["sale.order"].search([])
        purchases2 = self.env["purchase.order"].search([])
        factures2 = self.env["account.move"].search([])
        for s in sales:
            if s.projet:
               s.projet.devis = [(4, s.id)]
        for p in purchases:
            if p.projet:
               p.projet.achats = [(4, p.id)]
        for a in factures:
            if a.projet:
               a.projet.factures = [(4, a.id)]
	for s2 in sales2:
            if s2.state == "cancel":
                s2.projet = False
        for p2 in purchases2:
            if p2.state == "cancel":
                p2.projet = False
        for a2 in factures2:
            if a2.state == "cancel":
                a2.projet = False
        projets = self.env["project.project"].search([])
        for proj in projets:
            for dev in proj.devis:
                 if dev.state == "cancel":
                      proj.devis = [(3, dev.id)]
		      dev.projet = False
            for achat in proj.achats:
                 if achat.state == "cancel":
                      proj.achats = [(3, achat.id)]
		      achat.projet = False
            for fact in proj.factures:
                 if fact.state == "cancel":
                      proj.factures = [(3, fact.id)]
		      fact.projet = False
            for fact_f in proj.factures_fournisseurs:
                 if fact_f.state == "cancel":
                      proj.factures_fournisseurs = [(3, fact_f.id)]
		      dev.fact_f = False	
    def _get_all_documents(self):
        self.all_documents  = [document.id for document in self.projet.all_documents]

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

    def generate_documents(self):

        
        dossier = os.path.dirname(__file__)
        bati_attestation = dossier +  "/../static/documents/Batiavenir_Attestation_Travaux.pdf"
        b2m_attestation= dossier + "/../static/documents/B2M_Attestation_Travaux.pdf"

        data_attestation = {

            'Nom_Entreprise': self.partner_id.name,
            'Adresse_Entreprise': self.partner_id.street + ", " + self.partner_id.city + ", " +self.partner_id.country_id.name,
            'Adresse_Entreprise 5': 'Adresse_Entreprise 5',
            'Nom_Entreprise 5': 'Nom_Entreprise 5',
            'Nom_Entreprise 6': 'Nom_Entreprise 6',
            'Nom_Entreprise 7': 'Nom_Entreprise 7',
            'Adresse_Entreprise 6': 'Adresse_Entreprise 6',
            'Nom_Entreprise 1': self.partner_id.name,
            'Adresse_Entreprise 1': self.partner_id.street + ", " + self.partner_id.city + ", " +self.partner_id.country_id.name,
            'Nom_Entreprise 2':self.partner_id.project_manager.name,
            'Adresse_Entreprise 2': self.partner_id.project_manager.street + ", " + self.partner_id.project_manager.city + ", " +self.partner_id.project_manager.country_id.name,
            'Nom_Entreprise 3':self.partner_id.technical_controller.name ,
            # 'Nom_Entreprise 4': 'Nom_Entreprise 4',
            'Adresse_Entreprise 3':  self.partner_id.technical_controller.street + ", " + self.partner_id.technical_controller.city + ", " +self.partner_id.technical_controller.country_id.name,
            'Adresse_Entreprise 4': 'Adresse_Entreprise 4',
            'Nom_Entreprise 8': 'Nom_Entreprise 8',
            'Nom_Entreprise 9': 'Nom_Entreprise 9',
            'Adresse_Entreprise 7': 'Adresse_Entreprise 7',


        }
        
        
        default_dict_attestation = {
            'Nom_Entreprise': data_attestation.get('Nom_Entreprise', ''),
            'Adresse_Entreprise': data_attestation.get('Adresse_Entreprise', ''),
            'Adresse_Entreprise 5': data_attestation.get('Adresse_Entreprise 5', ''),
            'Nom_Entreprise 5': data_attestation.get('Nom_Entreprise 5', ''),
            'Nom_Entreprise 6': data_attestation.get('Nom_Entreprise 6', ''),
            'Nom_Entreprise 7': data_attestation.get('Nom_Entreprise 7', ''),
            'Adresse_Entreprise 6': data_attestation.get('Adresse_Entreprise 6', ''),
            'Nom_Entreprise 1': data_attestation.get('Nom_Entreprise 1', ''),
            'Adresse_Entreprise 1': data_attestation.get('Adresse_Entreprise 1', ''),
            'Nom_Entreprise 2': data_attestation.get('Nom_Entreprise 2', ''),
            'Adresse_Entreprise 2': data_attestation.get('Adresse_Entreprise 2', ''),
            'Nom_Entreprise 3': data_attestation.get('Nom_Entreprise 3', ''),
            'Nom_Entreprise 4': data_attestation.get('Nom_Entreprise 4', ''),
            'Adresse_Entreprise 3': data_attestation.get('Adresse_Entreprise 3', ''),
            'Adresse_Entreprise 4': data_attestation.get('Adresse_Entreprise 4', ''),
            'Nom_Entreprise 8': data_attestation.get('Nom_Entreprise 8', ''),
            'Nom_Entreprise 9': data_attestation.get('Nom_Entreprise 9', ''),
            'Adresse_Entreprise 7': data_attestation.get('Adresse_Entreprise 7', ''),
        }

        bati_proces = dossier +  "/../static/documents/Batiavenir_Proces_Verbal_Reception.pdf"
        b2m_proces= dossier +  "/../static/documents/B2M_Proces_Verbal_Reception.pdf"

        data_proces_verbal= {
            "Nom_Entreprise": self.partner_id.name,
            "Adresse_Entreprise": self.partner_id.street + ", " + self.partner_id.city + ", " +self.partner_id.country_id.name,
            "Nom": self.partner_id.project_manager.name,
            # "Concernant": 'Concernant',
            # "Relatif à": 'Relatif à',
            # "Concernant 1": 'Concernant 1',
            # "Concernant 2": 'Concernant 2',
            # "Relatif à 1": 'Relatif à 1',
            # "Concernant 3": 'Concernant 3',
            # "Concernant 4": 'Concernant 4',
        }

        default_dict_proces_verbal = {
            "Nom_Entreprise": data_proces_verbal.get('Nom_Entreprise', ''),
            "Adresse_Entreprise": data_proces_verbal.get('Adresse_Entreprise', ''),
            "Nom": data_proces_verbal.get('Nom', ''),
            "Concernant": data_proces_verbal.get('Concernant', ''),
            "Relatif à": data_proces_verbal.get('Relatif à', ''),
            "Concernant 1": data_proces_verbal.get('Concernant 1', ''),
            "Concernant 2": data_proces_verbal.get('Concernant 2', ''),
            "Relatif à 1": data_proces_verbal.get('Relatif à 1', ''),
            "Concernant 3": data_proces_verbal.get('Concernant 3', ''),
            "Concernant 4": data_proces_verbal.get('Concernant 4', ''),

        }

        attestations = [bati_attestation, b2m_attestation]
        process = [b2m_proces, bati_proces]


        for attestation in attestations:
            f, filename = tempfile.mkstemp()
            self.fill_pdf(attestation,  filename, default_dict_attestation)
            attachment_id = self.create_attachment_from_pdf(attestation.split("/")[-1], filename,self.id)
            self.piece_joint = [(4, attachment_id.id)]

        url  = ""
        for proces in process:
            f, filename = tempfile.mkstemp()
            self.fill_pdf(proces, filename, default_dict_proces_verbal)
            attachment_id = self.create_attachment_from_pdf(proces.split("/")[-1], filename, self.id)
            self.piece_joint = [(4, attachment_id.id)]
            url = attachment_id.local_url

     # code snipet for downloading zip file
        return {
                'type': 'ir.actions.act_url',
                "url" : url,
                'target': 'new',
        }


    def create_attachment_from_pdf(self,name, file, id):
        c = open(file, "rb").read()
        return self.env['ir.attachment'].create({
        'name': name,
        'type': 'binary',
        'datas': base64.encodestring(c),
        "public" :  True,
        "res_id" : id,
        "res_model" : "sale.order",

    })

	# @api.onchange('projet')
    # def _onchange_projet(self):
    #     dataa = self.env['sale.order'].browse(self._context.get('active_ids',[]))
    #     self.projet.devis = [(4, dataa.id)]


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"


    def _default_document(self):
        dossier = os.path.dirname(__file__)
        attestation_tva = dossier +  "/../static/documents/document_obligatoire_tva.pdf"
        c = open(attestation_tva, "rb").read()
        c = open(attestation_tva, "r").read()
        return base64.encodestring(c)


    attestation_simplifiee = fields.Binary()
    attestation_simplifiee_name = fields.Char(default="document_obligatoire_tva_modele.pdf")
    attestation_signee = fields.Boolean("signé?")

    is_manager = fields.Boolean('Administrateur',compute="_get_groups_access")
    project_manager = fields.Many2one('res.partner')
    technical_controller = fields.Many2one('res.partner')


    def _get_groups_access(self):
        for record in self:
            record.is_manager = self.env.user.has_group('account.group_account_manager')


class Ajouter_projet(models.TransientModel):
    _name = 'ajouter.projet'
    _description = "Ajouter projet"

    projet = fields.Many2one('project.project', string='Projets', required=True)


    def action_add_projet(self):
        dataa = self.env['sale.order'].browse(self._context.get('active_ids', []))
        dataa.projet = self.projet.id
        self.projet.devis = [(4, dataa.id)]
        self.projet.reference_chantier = dataa.x_reference


class projectttt(models.Model):
    _inherit = 'purchase.order'

    projet = fields.Many2one('project.project', "Projet", help="Reference to Project")

    # @api.onchange('projet')
    # def _onchange_projet(self):

    #     dataa = self.env['sale.order'].browse(self._context.get('active_ids',[]))

    #     self.projet.devis = [(4, dataa.id)]


class Ajouter_projet_achat(models.TransientModel):
    _name = 'ajouter.projet.achats'
    _description = "Ajouter projet"

    projet = fields.Many2one('project.project', string='Projets', required=True)

    def action_add_projet(self):
        dataa = self.env['purchase.order'].browse(self._context.get('active_ids', []))

        dataa.projet = self.projet.id
        self.projet.achats = [(4, dataa.id)]


class projectttt(models.Model):
    _inherit = 'account.move'

    projet = fields.Many2one('project.project', "Projet", help="Reference to Project")


    all_documents =  fields.Many2many("ir.attachment",
                                      compute="_get_all_documents"
    )

    def _get_all_documents(self):
        self.all_documents  = [document.id for document in self.projet.all_documents]

class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    attachment_ids_additional = fields.Many2many(
        'ir.attachment', 'mail_compose_message_ir_attachments_additional_rel',
        'wizard_id', 'attachment_id', 'Attachments Additional', )

    partner_ids = fields.Many2many('res.partner', string='Recipients', context={'active_test': False})


    @api.onchange("invoice_ids")
    def get_attachment_ids_additional(self):
        res_ids = self._context.get('active_ids')
        invoices = self.env['account.move'].browse(res_ids)
        for inv in invoices:
            for piece_joint in inv.piece_joint:
                if piece_joint.joindre_mail:
                    self.attachment_ids_additional = [(4, piece_joint.id)]


    def  send_and_print_action(self):
            for attachment_id in self.attachment_ids_additional :
                self.attachment_ids = [(4, attachment_id.id)]
            return super(AccountInvoiceSend, self).send_and_print_action()


    def get_problemes(self):
        res = {'warning': {
            'title': _('Warning'),
            'message': _('My warning message.')
        }}
        if res:
            return res



class Ajouter_projet_achat(models.TransientModel):
    _name = 'ajouter.projet.moves'
    _description = "Ajouter projet"

    projet = fields.Many2one('project.project', string='Projets', required=True)

    def action_add_projet(self):
        dataa = self.env['account.move'].browse(self._context.get('active_ids', []))
        dataa.projet = self.projet.id
        self.projet.factures = [(4, dataa.id)]


class Ajouter_factures_project(models.TransientModel):
    _name = 'ajouter.factures.projectt'
    _description = "Ajouter factures"

    factures = fields.Many2one('account.move', string='Facture', required=True, domain=[("type", "=", "out_invoice")])

    def action_add_projet(self):
        data = self.env['project.project'].browse(self._context.get('active_id', []))
        data.factures = [(4, self.factures.id)]
        self.factures.projet = data.id



class Ajouter_factures_fournisseur_project(models.TransientModel):
    _name = 'ajouter.factures_fournisseur.project'
    _description = "Ajouter factures fournisseur"

    factures_fournisseurs = fields.Many2one('account.move', string='Facture Fournisseur', required=True, domain = lambda self: self.get_domain_facture_fournisseur())


    def get_domain_facture_fournisseur(self):

        liste_invoices = []
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        bdc_origin = self.env["purchase.order"].search([("projet.id", "=", data.id)])
        for  bdc in bdc_origin:
                liste_invoices = liste_invoices + [invoice.id for invoice in self.env["account.move"].search([("invoice_origin", '=', bdc.name),('type', '=', 'in_invoice'), ("state", 'in', ("draft","posted","cancel"))])]
        return [('id', 'in',liste_invoices)]


    def action_add_projet(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        data.factures_fournisseurs = [(4, self.factures_fournisseurs.id)]
        self.factures_fournisseurs.projet = data.id

class Ajouter_devis_project(models.TransientModel):
    _name = 'ajouter.devis.projectt'
    _description = "Ajouter devis"

    devis = fields.Many2one('sale.order', string='Devis', required=True)

    def action_add_projet(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))

        data.devis = [(4, self.devis.id)]
        self.devis.projet = data.id
        data.reference_chantier = self.devis.x_reference


class delier_achat_projet(models.TransientModel):
    _name = 'delier.achat.projet'
    _description = "delier Achat"

    achat = fields.Many2one('purchase.order', string='Achats', required=True)

    @api.onchange('achat')
    def _getfilter(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        return {'domain': {'achat': [('id', 'in', data.achats.ids)]}}

    def action_delier_achat(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        for m in data:
            self.achat.projet = False
            m.achats = [(3, self.achat.id)]


class delier_devis_projet(models.TransientModel):
    _name = 'delier.devis.projet'
    _description = "delier devis"

    devis = fields.Many2one('sale.order', string='Devis', required=True)

    @api.onchange('devis')
    def _getfilter(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        return {'domain': {'devis': [('id', 'in', data.devis.ids)]}}

    def action_delier_devis(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        for m in data:
            self.devis.projet = False
            m.devis = [(3, self.devis.id)]


class delier_fact_projet(models.TransientModel):
    _name = 'delier.fact.projet'
    _description = "delier fact"

    facture = fields.Many2one('account.move', string='facture', required=True,domain=lambda self:self._getfilter())

    @api.onchange('facture')
    def _getfilter(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        return {'domain': {'facture': [('id', 'in', data.factures.ids)]}}

    def action_delier_fact(self):
        data = self.env['project.project'].browse(self._context.get('active_ids', []))
        for m in data:
            self.facture.projet = False
            m.factures = [(3, self.facture.id)]



