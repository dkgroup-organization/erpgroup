from odoo import models, fields, api
from datetime import timedelta, datetime

import logging
_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = "project.project"

    #reference_chantier = fields.Char(string="Chantier Ref")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
