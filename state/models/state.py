# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xml.etree.ElementTree as xee
from odoo import api, exceptions, fields, models, _
from datetime import datetime

class State(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
            ('cede', 'Cédé'),
        ], string='Status', required=True, readonly=False, copy=False, tracking=True, store=True, index=True,
        default='draft')
    invoice_payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')],
        string='Payment', store=True, readonly=False, copy=False, tracking=True,
        compute='_compute_amount')
    type = fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], string='Type', required=False, store=True, index=True, readonly=False, tracking=True,
        default="entry", change_default=True)
    date_invoice = fields.Date(string='Invoice Date',
        readonly=True, states={'draft': [('readonly', False)]}, index=True,
        help="Keep empty to use the current date", copy=False, default=datetime.now().strftime('%Y-%m-%d'))
    invoice_origin = fields.Char(string='Origin', readonly=False, tracking=True,
        help="The document(s) that generated the invoice.")
    x_nom_display = fields.Boolean('Masquer la colonne Article', default=True)
    x_reglement = fields.Selection([('cheque','Chèque'),('paypal','Paypal'),('vir','Virement bancaire'),('espece','Espèces'),('carte','Carte bancaire'),('prelev','Prélévement')],index=True, readonly=False,store=True,related='x_sale_id.x_reglement')

    invoice_payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        readonly=True, states={'draft': [('readonly', False)]})
    # @api.model
    # def _default_term(self):
    #     return self.partner_id.property_payment_term_id

class Statepurchase(models.Model):
    _inherit = 'purchase.order'

    # state = fields.Selection([
    #     ('draft', 'RFQ'),
    #     ('sent', 'RFQ Sent'),
    #     ('to approve', 'To Approve'),
    #     ('purchase', 'Purchase Order'),
    #     ('done', 'Locked'),
    #     ('cancel', 'Cancelled')
    # ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)
    x_nom_display = fields.Boolean('Masquer la colonne Article', default=True)

class product_template(models.Model):
    _inherit = 'product.template'
    company_id = fields.Many2one(
        'res.company', 'Company', index=1,default=lambda self: self.env.company)

class Statesale(models.Model):
    _inherit = 'sale.order'


    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=False, copy=False, index=True, tracking=3, default='draft')
    x_nom_display = fields.Boolean('Masquer la colonne Article',default=True)
    invoice_ids = fields.Many2many("account.move", string='Invoices', compute="_get_invoiced", readonly=False, copy=False, search="_search_invoice_ids",store=True)
    factures = fields.Many2many("account.move",'accountt_mmove_rrel', string='fact_import', readonly=False, copy=False,store=True)
    invoice_status = fields.Selection([
        ('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
        ], string='Invoice Status', compute='_get_invoice_status', store=True, readonly=False)
    x_reglement = fields.Selection([('cheque','Chèque'),('paypal','Paypal'),('vir','Virement bancaire'),('espece','Espèces'),('carte','Carte bancaire'),('prelev','Prélévement')],index=True, readonly=False,store=True)


    # def action_confirm(self):

    #     res = super(Statesale, self).action_confirm()

    #     for do_pick in self.picking_ids:

    #         do_pick.x_contact = self.x_contact
    #         do_pick.x_objet = self.x_objet
    #         do_pick.user_id = self.user_id

        # return res

class AccountInvoiceLine2(models.Model):
    _inherit = "account.move.line"

    discount = fields.Float(string='Discount (%)', digits=(16, 2), default=0.0)

class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'
    is_print = fields.Boolean('Print', default=False)



# class SaleOrderLine(models.Model):

#     _inherit = "sale.order.line"

#     tax_id = fields.Many2many('account.tax', string='Taxes', default= '20', domain=['|', ('active', '=', False), ('active', '=', True)])

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

  
     


    
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', default= lambda self: self.env['product.product'].search([('name','=','Ligne')]))
    name = fields.Text(string='Description                  .', required=True )





# class adddfields_parc(models.Model):
#     _inherit = 'fleet.vehicle'

#     # driver_id = fields.Many2one('res.partner', 'Driver', tracking=True, help='Driver of the vehicle', copy=False)
#     # future_driver_id = fields.Many2one('res.partner', 'Future Driver', tracking=True, help='Next Driver of the vehicle')

#     driver_id2 = fields.Many2one('hr.employee', string="Driver",help='Driver of the vehicle', copy=False,tracking=True)

#     future_driver_id2 = fields.Many2one('hr.employee', string="Future Driver", help='Next Driver of the vehicle', tracking=True)



class pose_infffo(models.Model):
    _inherit = 'project.project'

    pieces_joint = fields.Many2many('ir.attachment','project_project_rel2', string='Piéces jointes', store=True)



class Paymenets(models.Model):
    _inherit = 'account.payment'
    name = fields.Char(readonly=False, copy=False)  # The name is attributed upon post()
    payment_reference = fields.Char(copy=False, readonly=False, help="Reference of the document used to issue this payment. Eg. check number, file name, etc.")
    move_name = fields.Char(string='Journal Entry Name', readonly=False,
        default=False, copy=False,
        help="Technical field holding the number given to the journal entry, automatically set when the statement line is reconciled then stored to set the same number again if the line is cancelled, set to draft and re-processed again.")

    # Money flows from the journal_id's default_debit_account_id or default_credit_account_id to the destination_account_id
    destination_account_id = fields.Many2one('account.account', compute='_compute_destination_account_id', readonly=False)
    # For money transfer, money goes from journal_id to a transfer account, then from the transfer account to destination_journal_id
    destination_journal_id = fields.Many2one('account.journal', string='Transfer To', domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', company_id)]", readonly=False, states={'draft': [('readonly', False)]})

    invoice_ids = fields.Many2many('account.move', 'account_invoice_payment_rel', 'payment_id', 'invoice_id', string="Invoices", copy=False, readonly=False,
                                   help="""Technical field containing the invoice for which the payment has been generated.
                                   This does not especially correspond to the invoices reconciled with the payment,
                                   as it can have been generated first, and reconciled later""")
    reconciled_invoice_ids = fields.Many2many('account.move', string='Reconciled Invoices', compute='_compute_reconciled_invoice_ids', help="Invoices whose journal items have been reconciled with these payments.")
    has_invoices = fields.Boolean(compute="_compute_reconciled_invoice_ids", help="Technical field used for usability purposes")
    reconciled_invoices_count = fields.Integer(compute="_compute_reconciled_invoice_ids")

    move_line_ids = fields.One2many('account.move.line', 'payment_id', readonly=False, copy=False, ondelete='restrict')
    move_reconciled = fields.Boolean(compute="_get_move_reconciled", readonly=False)

    state = fields.Selection([('draft', 'Draft'), ('posted', 'Validated'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], readonly=False, default='draft', copy=False, string="Status")
    payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money'), ('transfer', 'Internal Transfer')], string='Payment Type', required=True, readonly=False, states={'draft': [('readonly', False)]})
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', required=True, readonly=False, states={'draft': [('readonly', False)]},
        help="Manual: Get paid by cash, check or any other method outside of Odoo.\n"\
        "Electronic: Get paid automatically through a payment acquirer by requesting a transaction on a card saved by the customer when buying or subscribing online (payment token).\n"\
        "Check: Pay bill by check and print it from Odoo.\n"\
        "Batch Deposit: Encase several customer checks at once by generating a batch deposit to submit to your bank. When encoding the bank statement in Odoo, you are suggested to reconcile the transaction with the batch deposit.To enable batch deposit, module account_batch_payment must be installed.\n"\
        "SEPA Credit Transfer: Pay bill from a SEPA Credit Transfer file you submit to your bank. To enable sepa credit transfer, module account_sepa must be installed ")
    payment_method_code = fields.Char(related='payment_method_id.code',
        help="Technical field used to adapt the interface to the payment type selected.", readonly=False)

    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor')], tracking=True, readonly=False, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', string='Partner', tracking=True, readonly=False, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    amount = fields.Monetary(string='Amount', required=True, readonly=False, states={'draft': [('readonly', False)]}, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=False, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    payment_date = fields.Date(string='Date', default=fields.Date.context_today, required=True, readonly=False, states={'draft': [('readonly', False)]}, copy=False, tracking=True)
    communication = fields.Char(string='Memo', readonly=False, states={'draft': [('readonly', False)]})
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=False, states={'draft': [('readonly', False)]}, tracking=True, domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', company_id)]")
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=False)

    hide_payment_method = fields.Boolean(compute='_compute_hide_payment_method',
                                         help="Technical field used to hide the payment method if the "
                                         "selected journal has only one available which is 'manual'")

    payment_difference = fields.Monetary(compute='_compute_payment_difference', readonly=False)
    payment_difference_handling = fields.Selection([('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')], default='open', string="Payment Difference Handling", copy=False)
    writeoff_account_id = fields.Many2one('account.account', string="Difference Account", domain="[('deprecated', '=', False), ('company_id', '=', company_id)]", copy=False)
    writeoff_label = fields.Char(
        string='Journal Item Label',
        help='Change label of the counterpart that will hold the payment difference',
        default='Write-Off')
    partner_bank_account_id = fields.Many2one('res.partner.bank', string="Recipient Bank Account", readonly=False, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    show_partner_bank_account = fields.Boolean(compute='_compute_show_partner_bank', help='Technical field used to know whether the field `partner_bank_account_id` needs to be displayed or not in the payments form views')
    require_partner_bank_account = fields.Boolean(compute='_compute_show_partner_bank', help='Technical field used to know whether the field `partner_bank_account_id` needs to be required or not in the payments form views')
    factures = fields.Many2many('account.move', 'account_factures_payment_rel', string="fact_fact", copy=False, readonly=False)
