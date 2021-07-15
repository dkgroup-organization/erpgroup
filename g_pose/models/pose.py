from odoo import api, fields, models, _

class pose_info(models.Model):
    _inherit = 'project.task'

    
    @api.model
    def _get_default_tele(self):
        if 'default_project_id' in self.env.context:
            default_project_id = self.env['project.project'].browse(self.env.context['default_project_id'])
            return default_project_id.exists().partner_id.phone
    @api.model
    def _get_default_ref(self):
        if 'default_project_id' in self.env.context:
            default_project_id = self.env['project.project'].browse(self.env.context['default_project_id'])
            return default_project_id.exists().reference_chantier


    @api.model
    def _get_default_lieu(self):
        if 'default_project_id' in self.env.context:
            default_project_id = self.env['project.project'].browse(self.env.context['default_project_id'])
            return default_project_id.exists().partner_id.contact_address


    

    photos = fields.Many2many('ir.attachment','vehiii_rel', string='Photos', required = False)
    reference_chantier = fields.Char('Reference Chantier',readonly=False,default=lambda self: self._get_default_ref())
    tele = fields.Char('Telephone',readonly=False, default=lambda self: self._get_default_tele())
    lieu_intervention = fields.Char('Adresse',readonly=False,default=lambda self: self._get_default_lieu())
    heure_arrive = fields.Char('Heure d\'arrivé')
    commerciale  = fields.Many2one(
        'res.users', string='commercial',
        default=lambda self: self.env.uid,
        ondelete='restrict')

    equipe = fields.Many2many('hr.employee','equipe_rel', string='Equipe d\'intervention')
    vehicule = fields.Many2many('fleet.vehicle','vehi_rel', string='Véhicule')
    pieces_joint = fields.Many2many('ir.attachment', string='Piéces jointes', store=True)

    state = fields.Selection([
            ('draft', 'En cours'),
            ('repo', 'Reporté'),
            ('done', 'Terminé'),
            ('cancel', 'Annuler'),
            ],default='draft')
    
    def repo(self):
        self.write({
        'state': 'repo',
    })
    
    def done(self):
        self.write({
        'state': 'done',
          })
        self.action_timer_stop()

        return {
            'name': _('Ajouter photos'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ajouter.photo',
            'view_id': self.env.ref('g_pose.view_add_photo_wizard_form').id,
            'target': 'new',
            # 'context': ctx,
        }
    def cancel(self):
        self.write({
        'state': 'cancel',
    })
    def draft(self):
        self.write({
        'state': 'draft',
    })





class Ajouter_photo(models.TransientModel):
        _name = 'ajouter.photo'
        _description = "Ajouter Photo"   

        photos = fields.Many2many('ir.attachment', string='Photos', required = True)
        
        def action_add_photo(self):
            dataa = self.env['project.task'].browse(self._context.get('active_ids',[]))

            for m in self.photos:
                dataa.photos = [(4, m.id)]
           


    