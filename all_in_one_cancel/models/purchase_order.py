from odoo import api, fields, models, exceptions


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    cancel_done_picking = fields.Boolean(string='Cancel Done Delivery?', compute='check_cancel_done_picking')
    cancel_paid_invoice = fields.Boolean(string='Cancel Paid Bill?', compute='check_cancel_paid_bill')

    @api.model
    def check_cancel_paid_bill(self):
        for order in self:
            Flag = False
            if order.company_id.cancel_paid_invoice and order.invoice_count > 0:
                for invoice in self.invoice_ids:
                    if invoice.state != 'cancel':
                        Flag = True
                        break
            order.cancel_paid_invoice = Flag
    
    def cancel_invoice(self):
        invoices=[]
        invoice_obj = self.env['account.move']
        for invoice in self.invoice_ids:
            if invoice.state !='cancel':
                invoices.append(invoice.id)
        if invoices:
            if len(invoices) == 1 :
                print(invoices)
                invoice = invoice_obj.browse(invoices[0])
                invoice.with_context({'Flag':True}).button_cancel()
                return self.action_view_bill_for_app(invoice)
            else:
                return self.action_cancel_selected_invoice(invoices)
        
    def action_view_bill_for_app(self, invoice):

        action = self.env.ref('account.action_move_in_invoice_type').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = invoice.id
        return action

    def action_cancel_selected_invoice(self, invoices):
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.invoice.wizard',
            'view_mode':'form',
            'views': [(self.env.ref('all_in_one_cancel.invoice_cancel_form_cft_all_in_one_cancel').id, 'form')],
            'target': 'new',
            'context': {
                    'invoices':invoices,
            },
        }

    @api.model
    def check_cancel_done_picking(self):
        for order in self:
            Flag = False
            if order.company_id.cancel_done_picking and order.picking_count > 0:
                for picking in self.picking_ids:
                    if picking.state != 'cancel':
                        Flag = True
                        break
            order.cancel_done_picking = Flag

    def cancel_picking(self):
        if len(self.picking_ids) == 1 :
            self.picking_ids.with_context({'Flag':True}).action_cancel()
            return self.action_view_delivery()
        else:
            return self.action_cancel_selected_picking()
        
    def action_view_delivery(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        picking_records = self.mapped('picking_ids')
        if picking_records:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = picking_records.id
        return action

    def action_cancel_selected_picking(self):
        picking_obj=self.env['stock.picking']
        pickings=[]
        for picking in self.picking_ids:
            if picking.state !='cancel':
                pickings.append(picking.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.picking.wizard',
            'view_mode':'form',
            'views': [(self.env.ref('all_in_one_cancel.delivery_cancel_form_cft_all_in_one_cancel').id, 'form')],
            'target': 'new',
            'context': {
                    'pickings':pickings,
            },
        }

    def button_cancel(self):
        quant_obj = self.env['stock.quant']
        model_obj = self.env['ir.model']
        moves = self.env['account.move']
        account_move_obj = self.env['account.move']
        model = model_obj.search([('model', '=', 'stock.landed.cost')])

        for order in self:
            if order.picking_ids and order.company_id.cancel_delivery_order_for_po :
                for picking in order.picking_ids:
                    if picking.state == 'cancel':
                        continue
                    if model and picking.picking_type_code == 'incoming':
                        cost_recs = self.env['stock.landed.cost'].search([('state', '=', 'done'),('picking_ids', 'in', order.picking_ids.ids)])
                        if cost_recs:
                            raise exceptions.Warning('Please Remove stock landed cost "%s" related with this incoming shipment(%s) then try to cancel it.'%(','.join(cost_recs.mapped('name')),picking.name))
                    if picking.state not in ['done']:
                        picking.action_cancel()
                    else:
                        account_moves = picking.move_lines
                        for move in account_moves:
                            if move.state == 'cancel':
                                continue
                            # move._do_unreserve()
                            if move.state == "done" and move.product_id.type == "product":
                                for move_line in move.move_line_ids:
                                    quantity = move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id)
                                    quant_obj._update_available_quantity(move_line.product_id, move_line.location_id, quantity,move_line.lot_id)
                                    quant_obj._update_available_quantity(move_line.product_id, move_line.location_dest_id, quantity * -1,move_line.lot_id)
                            if move.procure_method == 'make_to_order' and not move.move_orig_ids:
                                move.state = 'waiting'
                            elif move.move_orig_ids and not all(orig.state in ('done', 'cancel') for orig in move.move_orig_ids):
                                move.state = 'waiting'
                            else:
                                move.state = 'confirmed'
                            siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
                            if move.propagate_cancel:
                                # only cancel the next move if all my siblings are also cancelled
                                if all(state == 'cancel' for state in siblings_states):
                                    move.move_dest_ids._action_cancel()
                            else:
                                if all(state in ('done', 'cancel') for state in siblings_states):
                                    move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                                move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
                            account_moves = account_move_obj.search([('stock_move_id', '=', move.id)])
                            valuation = move.stock_valuation_layer_ids
                            valuation and valuation.sudo().unlink()
                            if account_moves:
                                for account_move in account_moves:
                                    account_move.button_cancel()
                                    account_move.unlink()

            if order.company_id.cancel_invoice_for_po:
                for invoice in order.invoice_ids:
                    if invoice.journal_id and not invoice.journal_id.restrict_mode_hash_table:
                        invoice.journal_id.write({'restrict_mode_hash_table':False})
                    if invoice.state in ['draft','cancel']:
                        invoice.button_cancel()

                    else:
                        
                        if invoice and not invoice.journal_id.restrict_mode_hash_table:
                            invoice.write({'restrict_mode_hash_table':False})
                        invoice.button_cancel()

        res = super(PurchaseOrder,self).button_cancel()
        return res
