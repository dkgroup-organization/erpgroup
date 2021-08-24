# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


    def print_report(self):
        report=self.env.ref('ay_ma_payroll.report_status_transfer').report_action(self)
        return report

    def get_form(self):
        return {
            'name': 'Configuration Rapport',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'report.certificate',
            'target': 'new',
            'context':{'default_partner_id':self.partner_id.id,'default_company_id':3,'default_client_name':self.partner_id.name,'default_client_adress':self.partner_id.street}
#            'context': {'default_lieu': setting.lieu,'default_company_id': self.company_id.id,'default_n_compte':setting.n_compte.id if(setting.n_compte) else False,'default_objet':setting.objet if(setting.objet) else "Virement des salaires",'default_destinataire':setting.destinataire,'default_payslip_run_id':self.id,'default_titule_des':setting.titule_des,'default_date_start':date_start}
        }