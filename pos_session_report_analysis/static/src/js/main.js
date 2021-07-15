/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_session_report_analysis.pos_session_report_analysis',function(require){
    "use strict"
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var _t = core._t;
    var ajax = require('web.ajax');
    var CrashManager = require('web.CrashManager').CrashManager;
    var AbstractAction = require('web.AbstractAction');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var Printer = require('point_of_sale.Printer').Printer;


    var SessionReportButtonWidget = screens.ActionButtonWidget.extend({
        template: 'SessionReportButtonWidget',
        button_click: function() {
           var self = this;
           this.$el.click(function(){
            self.print_sale_details();
        });

                
        },

        print_sale_details: function () {
        var self = this;
        var printer = new Printer();
        rpc.query({
            model: 'report.point_of_sale.report_saledetails',
            method: 'get_sale_details',
            args: [false, false, false, [this.pos.pos_session.id]],
        })
        .then(function(result){
            var env = {
                widget: new PosBaseWidget(self),
                company: self.pos.company,
                pos: self.pos,
                products: result.products,
                payments: result.payments,
                taxes: result.taxes,
                total_paid: result.total_paid,
                date: (new Date()).toLocaleString(),
            };
            var report = QWeb.render('SaleDetailsReport', env);
            self.print_receipt(report);
        });
    },
        generate_wrapped_product_name: function(name) {
			var MAX_LENGTH =24;
			var wrapped = [];
			var name = name;
			var current_line = "";
	
			while (name.length > 0) {
				var space_index = name.indexOf(" ");
	
				if (space_index === -1) {
					space_index = name.length;
				}
	
				if (current_line.length + space_index > MAX_LENGTH) {
					if (current_line.length) {
						wrapped.push(current_line);
					}
					current_line = "";
				}
	
				current_line += name.slice(0, space_index + 1);
				name = name.slice(space_index + 1);
			}
	
			if (current_line.length) {
				wrapped.push(current_line);
			}
	
			return wrapped;
		},
    });


     screens.define_action_button({
        'name': 'Session Summary',
        'widget': SessionReportButtonWidget,
        'condition': function() {
            if(this.pos.config && this.pos.config.wk_print_session_summary)
                return this.pos.config.wk_print_session_summary;
            else
                return false
        },
    });
});