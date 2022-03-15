# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging,json
_logger = logging.getLogger(__name__)

class setting_setting_aydoo(models.TransientModel):
    _name = 'setting.setting'
    _description = 'Setting'

    journal = fields.Integer("journal")
    payment = fields.Integer("Payment")
    def update_crm_lead(self):
        leads = self.env['crm.lead'].search([('type','=','lead'),('company_id','=',36)])
        for l in leads:
            l.stage_lead_id =157
        return True

    def update_moves_amount(self):
        moves = self.env['account.move'].search([('type','in',('out_invoice','in_invoice')),('state','in',('draft','cancel'))])
        _logger.info("nbre de factures %s" % (len(moves)))
        i=0
        for p in moves:
            i+=1
            _logger.info("Eteration %s" % (i))
            _logger.info("N° factures est  %s est %s" % (p.name,p.id))
            p._compute_amount()


    def get_moves_list(self):
        moves = self.env['account.move'].search([('invoice_payment_state','=','paid'),('type','=','out_invoice'),('state','=',"posted")])
        moves_filtred = moves.filtered(lambda r: not json.loads(r.invoice_payments_widget))
        for move in moves_filtred:
            _logger.info("id %s json %s et type %s et date de creation %s" %(move.id,move.invoice_payments_widget,type(move.invoice_payments_widget),move.create_date))
            #creation automatique des paiments
            move.write({'amount_residual':move.amount_total})
            move._compute_amount()
            Payment = self.env['account.payment'].with_context(default_invoice_ids=[(4, move.id, 'None')])
#             payment = Payment.create({
#                 'payment_method_id': 1,
#                 'payment_type': 'inbound',
#                 'partner_type': 'customer',
#                 'partner_id': move.partner_id.id,
#                 'amount': move.amount_total,
#                 'journal_id': 41,
#                 'company_id': self.env.company.id,
#                 'currency_id': self.env.company.currency_id.id,
#                 'payment_difference_handling': 'reconcile',
# #                'writeoff_account_id': self.diff_income_account.id,
#             })
            pmt_wizard = self.env['account.payment'].with_context(active_model='account.move',
                                                                           active_ids=move.id,active_id=move.id).create({
                'payment_date': move.create_date,
                'journal_id': self.journal,
                'payment_method_id': self.payment,
                #'currency_id': self.env.company.currency_id.id,
                'amount': move.amount_total,
            })
            pmt_wizard.post()
            #pmt_wizard._create_payments()

            #move.write({'amount_residual':move.amount_total})
            #move._compute_amount()

        #raise UserError(" moves : %s ; filtered : %s "% (len(moves),len(moves_filtred)))

        #raise UserError("json %s et type %s" %(move.invoice_payments_widget,type(move.invoice_payments_widget)))
        #raise UserError(len(moves))
    def get_documents(self):
        docs = self.env['ir.attachment'].sudo().search([('res_id','=',0),('create_uid','!=',1)])
        _logger.info('nbre de documets est %s' %(len(docs)))
        factures = self.env['account.move']
        devis = self.env['sale.order']
        _logger.info('nbre de devis : %s et nbre de factures %s' %(len(devis),len(factures)))
        for doc in docs:
            facture = factures.sudo().search([('piece_joint','in',doc.id)])
            #facture =  factures.sudo().filtered(lambda r : doc.id in r.piece_joint.ids)
            devi = devis.sudo().search([('piece_joint','in',doc.id)])
            _logger.info('---------nbre de devi : %s et nbre de facture %s' % (len(devi), len(facture)))
            if(len(facture)>1):
                _logger.info('factures plus 1')
            if(len(devi)>1):
                _logger.info('devi plus 1')
            if(facture and devi):
                _logger.info("deux %s %s" %())
        raise UserError('nbre de documets est %s' %(len(docs)))
        return True
from collections import defaultdict
class IrAttachmentInherit(models.Model):
    _inherit = 'ir.attachment'


    @api.model
    def check(self, mode, values=None):
        """Restricts the access to an ir.attachment, according to referred model
        In the 'document' module, it is overridden to relax this hard rule, since
        more complex ones apply there.
        """
        if self.env.is_superuser():
            return True
        # collect the records to check (by model)
        model_ids = defaultdict(set)            # {model_name: set(ids)}
        require_employee = False
        if self:
            # DLE P173: `test_01_portal_attachment`
            self.env['ir.attachment'].flush(['res_model', 'res_id', 'create_uid', 'public', 'res_field'])
            self._cr.execute('SELECT res_model, res_id, create_uid, public, res_field FROM ir_attachment WHERE id IN %s', [tuple(self.ids)])
            for res_model, res_id, create_uid, public, res_field in self._cr.fetchall():
                if not self.env.is_system() and res_field:
                    raise AccessError(_("Sorry, you are not allowed to access this document."))
                if public and mode == 'read':
                    continue
                if not (res_model and res_id):
                    if create_uid != self._uid:
                        require_employee = True
                    continue
                model_ids[res_model].add(res_id)
        if values and values.get('res_model') and values.get('res_id'):
            model_ids[values['res_model']].add(values['res_id'])

        # check access rights on the records
        for res_model, res_ids in model_ids.items():
            # ignore attachments that are not attached to a resource anymore
            # when checking access rights (resource was deleted but attachment
            # was not)
            if res_model not in self.env:
                require_employee = True
                continue
            elif res_model == 'res.users' and len(res_ids) == 1 and self._uid == list(res_ids)[0]:
                # by default a user cannot write on itself, despite the list of writeable fields
                # e.g. in the case of a user inserting an image into his image signature
                # we need to bypass this check which would needlessly throw us away
                continue
            records = self.env[res_model].browse(res_ids).exists()
            if len(records) < len(res_ids):
                require_employee = True
            # For related models, check if we can write to the model, as unlinking
            # and creating attachments can be seen as an update to the model
            access_mode = 'write' if mode in ('create', 'unlink') else mode
            records.check_access_rights(access_mode)
            records.check_access_rule(access_mode)

        if require_employee:
            if not (self.env.is_admin() or self.env.user.has_group('base.group_user')):
                raise AccessError(_("Sorry, you are not allowed to access this document."))


