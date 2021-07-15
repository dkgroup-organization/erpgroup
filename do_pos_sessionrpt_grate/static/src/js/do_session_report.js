odoo.define('do_pos_sessionrpt_grate.session_report', function (require) {
"use strict";

var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var ActionManager = require('web.ActionManager');

var QWeb = core.qweb;

var SessionReportPrintButton = screens.ActionButtonWidget.extend({
    template: 'SessionReportPrintButton',
    button_click: function(){
        var self = this;
        this.$el.click(function(){
            self.print_sale_details();
        });
    },

    /** Print an overview of todays sales.
     *
     * By default this will print all sales of the day for current PoS config.
     */
    print_sale_details: function () {
        var self = this;
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
            self.pos.proxy.printer.print_receipt(report);
        });
    },

});

screens.define_action_button({
    'name': 'session_report_print',
    'widget': SessionReportPrintButton,
    'condition': function(){ 
        return this.pos.config.do_session_report;
    },
});
return {
    SessionReportPrintButton: SessionReportPrintButton,
};
});