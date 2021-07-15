# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

    
class categoriess(models.Model):
   
    _inherit = 'pos.category'
    company_id = fields.Many2one('res.company', 'Company', required=False, index=True,store=True, default=lambda self: self.env.company)