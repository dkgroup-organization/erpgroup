

import re

import collections

from odoo import api, fields, models, _
from odoo.osv import expression

import werkzeug.urls


class respartnerbank(models.Model):
    _inherite = 'res.partner.bank'
    _sql_constraints = [
        ('unique_number', 'unique(sanitized_acc_number, company_id, partner_id)', 'Account Number must be unique'),
    ]