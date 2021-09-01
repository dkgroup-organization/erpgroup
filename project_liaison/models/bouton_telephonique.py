import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning



class AppelTelephoniqueModel(models.Model):
    _inherit = 'res.partner'


    def appel_telephonique(self):


        # external_id = "mail.mail_activity_view_form_popup"
        # model = "mail.activity"
        # view_name = "mail.activity.view.form.popup"
        return 1