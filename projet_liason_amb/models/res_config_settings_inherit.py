# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    company_works = fields.Many2one('res.partner')
    company_works_color = fields.Char(string="Couleur de société")

    def set_values(self):
        super(ResConfigSettingsInherit, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        a=self.company_works.id
        param.set_param('projet_liason_amb.company_works', a)
        param.set_param('projet_liason_amb.company_works_color', self.company_works_color)

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsInherit, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        test= param.get_param('projet_liason_amb.company_works')
        aa=False
        if(isinstance(test, (int))):
            aa=test
        res.update({
            'company_works': aa,
            'company_works_color':param.get_param('projet_liason_amb.company_works_color'),
        })
        return res


