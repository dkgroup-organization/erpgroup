# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, exceptions, fields, models, _

class joint(models.Model):
    _inherit = 'sale.order'

  
    
    piece_joint = fields.Many2many('ir.attachment', string='Piéces jointe', store=True)



class joint(models.Model):
    _inherit = 'account.move'



    piece_joint = fields.Many2many('ir.attachment', string='Piéces jointe', store=True)


class jointpiece(models.Model):
    _inherit = 'ir.attachment'

    joindre_mail = fields.Boolean( string="Joindre au Mail")
    datas = fields.Binary(string='File Content', compute='_compute_datas', inverse='_inverse_datas',readonly=False)
    db_datas = fields.Binary('Database Data', attachment=False,readonly=False)
    store_fname = fields.Char('Stored Filename',readonly=False)
    file_size = fields.Integer('File Size', readonly=False)
    checksum = fields.Char("Checksum/SHA1", size=40, index=True, readonly=False)
    mimetype = fields.Char('Mime Type', readonly=False)
    index_content = fields.Text('Indexed Content', readonly=False, prefetch=False)
    res_name = fields.Char('Resource Name', compute='_compute_res_name',readonly=False)
    res_model = fields.Char('Resource Model', readonly=False, help="The database object this attachment will be attached to.")
    res_field = fields.Char('Resource Field', readonly=False)
    res_id = fields.Many2oneReference('Resource ID', model_field='res_model',
                                      readonly=False, help="The record id this is attached to.")

