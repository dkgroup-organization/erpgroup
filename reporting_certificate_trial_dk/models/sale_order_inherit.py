# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'




    def get_form_work(self):
        return {
            'name': 'Configuration Rapport',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'report.certificate',
            'target': 'new',
            'view_id':self.env.ref('reporting_certificate_trial_dk.report_work_certificate_view_form').id,
            'context':{'default_partner_id':self.partner_id.id,'default_company_id':40,'default_client_name':self.partner_id.name,'default_client_adress':self.partner_id.street}
#            'context': {'default_lieu': setting.lieu,'default_company_id': self.company_id.id,'default_n_compte':setting.n_compte.id if(setting.n_compte) else False,'default_objet':setting.objet if(setting.objet) else "Virement des salaires",'default_destinataire':setting.destinataire,'default_payslip_run_id':self.id,'default_titule_des':setting.titule_des,'default_date_start':date_start}
        }

    def get_form_verbal(self):
        return {
                'name': 'Configuration Rapport',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id':self.env.ref('reporting_certificate_trial_dk.report_verbal_trial_view_form').id,
                'res_model': 'report.certificate',
                'target': 'new',
                'context': {'default_partner_id': self.partner_id.id, 'default_company_id': 40,
                            'default_client_name': self.partner_id.name,
                            'default_client_adress': self.partner_id.street}
                #            'context': {'default_lieu': setting.lieu,'default_company_id': self.company_id.id,'default_n_compte':setting.n_compte.id if(setting.n_compte) else False,'default_objet':setting.objet if(setting.objet) else "Virement des salaires",'default_destinataire':setting.destinataire,'default_payslip_run_id':self.id,'default_titule_des':setting.titule_des,'default_date_start':date_start}
        }