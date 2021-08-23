# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class joindre(models.Model):
    _inherit = 'fleet.vehicle'



    carte_grise = fields.Many2many('ir.attachment','vehiii_rel1', string='Carte Grise', required = False)
    assurance = fields.Many2many('ir.attachment','vehiii_rel2', string='Assurance', required = False)
    contrat = fields.Many2many('ir.attachment','vehiii_rel3', string='contravention', required = False)