# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _


class SaleSummaryReport(models.AbstractModel):
    _name = 'report.bi_pos_reports.report_sales_summary'

    def get_nested(self, data, *args):
        if args and data:
            element = args[0]
            if element:
                value = data.get(element)
                return value if len(args) == 1 else self.get_nested(value, *args[1:])

    def _get_report_values(self, docids, data=None):
        Report = self.env['ir.actions.report']
        sale_summary_rec = self.env['pos.sale.summary.wizard'].browse(docids)
        main_data_dict = {}
        summery_data = []
        journal = []
        categ = []
        categories_data = {}
        for u in sale_summary_rec.res_user_ids:
            user_name = u.name
            total, tax, discount = (False,) * 3
            sale_summary = self.env['pos.order'].search([
                ('date_order', '>=', sale_summary_rec.start_dt),
                ('date_order', '<=', sale_summary_rec.end_dt),
                ('user_id', 'in', user_name),
            ]).ids

            pos_line = self.env['pos.order.line'].search([('order_id.id', 'in', sale_summary)])

            for p in pos_line:
                prix = p.price_unit
                total = total + p.price_subtotal_incl
                discount += p.qty * p.price_unit - p.price_subtotal
                for t in p.tax_ids_after_fiscal_position:
                    tax = tax + ((t.amount * p.price_unit) / 100)

            summery_data.append({
                'name': u.name,
                'total': float(total),
                'tax': float(tax),
                'discount': float(discount),
                'prix': float(prix),
            })

            # ================================== JOURNAL ================================

            config_obj = self.env['pos.config'].search([])

            orders = self.env['pos.order'].search([
                ('date_order', '>=', sale_summary_rec.start_dt),
                ('date_order', '<=', sale_summary_rec.end_dt),
                ('state', 'in', ['paid', 'invoiced', 'done']),
                ('config_id', 'in', config_obj.ids),
                ('user_id', '=', user_name),
            ])

            statement_ids = self.env["account.bank.statement.line"].search([('pos_statement_id', 'in', orders.ids)]).ids

            if statement_ids:
                self.env.cr.execute("""
                    SELECT (journal.name) j_name, sum(amount) j_total
                    FROM account_bank_statement_line AS acc_state_line,
                        account_bank_statement AS acc_statement,
                        account_journal AS journal
                    WHERE acc_state_line.statement_id = acc_statement.id
                        AND acc_statement.journal_id = journal.id 
                        AND acc_state_line.id IN %s 
                    GROUP BY journal.name
				""", (tuple(statement_ids),))
                journal = self.env.cr.dictfetchall()
            else:
                journal = []

            # ================================== CATEGORY ================================

            product_ids = self.env["pos.order"].search([('id', 'in', orders.ids)]).ids

            if product_ids:
                self.env.cr.execute("""
				    SELECT (pc.name) c_name, sum(qty * price_unit) c_total
					FROM pos_order_line AS pol,
						 pos_category AS pc,
						 product_product AS product,
						 product_template AS templ
					WHERE pol.product_id = product.id
						AND templ.pos_categ_id = pc.id
						AND product.product_tmpl_id = templ.id
						AND pol.order_id IN %s 
					GROUP BY pc.name
					""", (tuple(product_ids),))
                categ = self.env.cr.dictfetchall()
            else:
                categ = []

            main_data_dict.update({u.name: {'journal': journal, 'categ': categ}})

        orders = self.env['pos.order'].search([
            ('date_order', '>=', sale_summary_rec.start_dt),
            ('date_order', '<=', sale_summary_rec.end_dt),
            ('state', 'in', ['paid', 'invoiced', 'done']),
        ])

        final_total = 0.0
        final_tax = 0.0
        final_discount = 0.0

        for order in orders:
            final_total += order.amount_total
            final_tax += order.amount_tax
            for line in order.lines:
                final_discount += line.qty * line.price_unit - line.price_subtotal
                category = line.product_id.pos_categ_id.name
                if not category:
                    category = "Unknown"
                if category in categories_data:
                    old_subtotal = categories_data[category]['total']
                    categories_data[category].update({
                        'total': old_subtotal + line.price_subtotal_incl,
                    })
                else:
                    categories_data.update({category: {
                        'name': category,
                        'total': line.price_subtotal_incl,
                    }})

            categories_tot = list(categories_data.values())
        st_line_ids = self.env["account.bank.statement.line"].search([('pos_statement_id', 'in', orders.ids)]).ids
        if st_line_ids:
            self.env.cr.execute("""
				SELECT aj.name, sum(amount) total
				FROM account_bank_statement_line AS absl,
					 account_bank_statement AS abs,
					 account_journal AS aj 
				WHERE absl.statement_id = abs.id
					AND abs.journal_id = aj.id 
					AND absl.id IN %s 
				GROUP BY aj.name
			""", (tuple(st_line_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []
        only_summary = sale_summary_rec.only_summary
        return {
            'currency_precision': 2,
            'doc_ids': docids,
            'doc_model': 'pos.sale.summary.wizard',
            'docs': sale_summary_rec.res_user_ids,
            'user_name': summery_data,
            'start_dt': sale_summary_rec.start_dt,
            'end_dt': sale_summary_rec.end_dt,
            'all_data': main_data_dict,
            'current_dt': datetime.now(),
            'journal': journal,
            'categ': categ,
            'only_summary': only_summary,
            'final_total': final_total,
            'final_tax': final_tax,
            'final_discount': final_discount,
            'payments': payments,
            'categories_data': categories_tot,
        }
