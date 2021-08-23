# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

rom odoo import api, fields, models, tools


class DecimalPprecision(models.Model):
    _inherit = 'decimal.precision'

    company_id2 = fields.Integer('Company',default=lambda self: self.env.user.company_id.id)
    digits = fields.Integer('Digits', required=True, compute='_compute_name')



    @api.depends('digits','company_id2')
    def _compute_name(self):
        for record in self:
        	if record.company_id2 == 1:
               record.digits = 4
            else:
               record.digits = 2