odoo.define('aspl_pos_direct_login_ee.pos', function (require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var framework = require('web.framework');
    var models = require('point_of_sale.models');
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;

    models.load_fields("res.users", ['login_with_pos_screen']);

    chrome.HeaderButtonWidget.include({
        renderElement: function(){
            var self = this;
            this._super();
            if(this.action){
                this.$el.click(function(){
                    self.gui.show_popup('confirm_close_pos_wizard');
                });
            }
        },
    });

    var ConfirmClosePosPopupWizard = PopupWidget.extend({
        template: 'ConfirmClosePosPopupWizard',
        show: function(){
            this._super();
            var self = this;
        },


        

        click_confirm: function(){
            var self = this;
            var id = self.pos.pos_session.id;

            var pro_st_date = this.$('#pro_st_date').val()
            var pro_ed_date = this.$('#pro_ed_date').val()
            var order = this.pos.get_order();
            var summery_product = [];
            var curr_session = self.pos.config.current_session_id[0];
            var prod_current_session = $('#prod_crnt_ssn').is(':checked')
            $('#prod_dt_strt').hide();
            $('#prod_dt_end').hide();

            if (prod_current_session == true) {
                rpc.query({
                    model: 'pos.order',
                    method: 'update_product_summery',
                    args: [order['sequence_number'], pro_st_date, pro_ed_date, prod_current_session, curr_session],
                })
                    .then(function (output_summery_product) {
                        summery_product = output_summery_product;
                        self.save_product_summery_details(output_summery_product, pro_st_date, pro_ed_date, prod_current_session);

                    });
            } else {
                if (ord_st_date == false) {
                    $('#prod_dt_strt').show()
                    setTimeout(function () {
                        $('#prod_dt_strt').hide()
                    }, 3000);
                    return
                } else if (ord_end_date == false) {
                    $('#prod_dt_end').show()
                    setTimeout(function () {
                        $('#prod_dt_end').hide()
                    }, 3000);
                    return
                } else {
                    rpc.query({
                        model: 'pos.order',
                        method: 'update_product_summery',
                        args: [order['sequence_number'], pro_st_date, pro_ed_date, prod_current_session, curr_session],
                    })
                        .then(function (output_summery_product) {
                            summery_product = output_summery_product;
                            self.save_product_summery_details(output_summery_product, pro_st_date, pro_ed_date, prod_current_session);

                        });
                }
            }






            rpc.query({
                model: 'pos.session',
                method: 'action_pos_session_closing_control',
                args: [id]
            }).then(function (result) {
                $('.session').trigger('click');
            }, function (err, event) {
                event.preventDefault();
                var err_msg = 'Please verify the details given or Check the Internet Connection./n';
                if (err.data.message)
                    err_msg = err.data.message;
                self.gui.show_popup('alert', {
                    'title': _t('Odoo Warning'),
                    'body': _t(err_msg),
                });
            });
            // var cashier = self.pos.user || false;
            // if(cashier && cashier.login_with_pos_screen){
            //     framework.redirect('/web/session/logout');
            // } else{
            //     self.pos.gui.close();
            // }
            
            this.gui.close_popup();
            
        },


    save_product_summery_details: function (output_summery_product, pro_st_date, pro_ed_date, prod_current_session) {
            var self = this;
            this.gui.close_popup();
            this.gui.show_screen('product_summery_receipt2', {
                output_summery_product: output_summery_product,
                pro_st_date: pro_st_date,
                pro_ed_date: pro_ed_date,
                prod_current_session: prod_current_session
            });
        },

    });
    gui.define_popup({name:'confirm_close_pos_wizard', widget: ConfirmClosePosPopupWizard});

});