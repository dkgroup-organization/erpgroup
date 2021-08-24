from odoo import api, fields, models, _

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
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
    )
    choice_1 = fields.Boolean('Attestation de travaux')
    choice_2 = fields.Boolean('Procés-Verbal')

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

    def get_report(self):
        report_work = self.env.ref('projet_liason_amb.report_work_certificate').report_action(self,config=False)
        report_verbal = self.env.ref('projet_liason_amb.report_verbal_trial').report_action(self,config=False)
        return (report_work,report_verbal)



