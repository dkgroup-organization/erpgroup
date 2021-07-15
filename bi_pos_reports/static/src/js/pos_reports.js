odoo.define('bi_pos_reports.pos', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var rpc = require('web.rpc');

    var QWeb = core.qweb;
    var _t = core._t;


    models.load_models({
        model: 'stock.location',
        fields: [],
        domain: null,
        loaded: function (self, locations) {
            self.locations = locations;

        },
    });

    models.load_models({
        model: 'pos.session',
        domain: null,
        loaded: function (self, pos_sessions) {
            self.pos_sessions = pos_sessions
        },
    });


    /*#################################################### Payment Summary ################################################################*/

    var ReportPaymentButtonWidget = screens.ActionButtonWidget.extend({
        template: 'ReportPaymentButtonWidget',

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
        },

        button_click: function () {
            var self = this;
            this._super();
            self.gui.show_popup('pos_payment_report_widget')
        },

        renderElement: function () {
            var self = this;
            this._super();
        },

    });


    screens.define_action_button({
        'name': 'Pos Payment Summary Widget',
        'widget': ReportPaymentButtonWidget,
        'condition': function () {
            return true;
        },
    });

    var PopupPaymentWidget = popups.extend({
        template: 'PopupPaymentWidget',

        init: function (parent, args) {
            var self = this;
            this._super(parent, args);
        },

        renderElement: function () {
            var self = this;
            this._super();
            $('#dt_strt').hide();
            $('#dt_end').hide();

            $('#pymnt_crnt_ssn').click(function () {
                if ($('#pymnt_crnt_ssn').is(':checked')) {
                    $('#strt_dt').hide();
                    $('#end_dt').hide();
                } else {
                    $('#strt_dt').show();
                    $('#end_dt').show();
                }
            });
            this.$('.print-payment').click(function () {
                self.render_payment_summary();
            });
        },

        render_payment_summary: function () {
            var self = this;
            var is_current_session = $('#pymnt_crnt_ssn').is(':checked')
            var pay_st_date = this.$('#pay_st_date').val()
            var pay_ed_date = this.$('#pay_ed_date').val()
            var smry_payment = this.$('#smry_payment').val()
            var order = this.pos.get_order();
            var curr_session = self.pos.config.current_session_id[0];
            var payment_summary = [];
            var cashier = this.pos.get_cashier();

            $('#dt_strt').hide();
            $('#dt_end').hide();

            if (is_current_session == true) {
                rpc.query({
                    model: 'pos.report.payment',
                    method: 'get_crnt_ssn_payment_pos_order',
                    args: [1, smry_payment, cashier.id, curr_session, is_current_session, pay_st_date, pay_ed_date],
                }).then(function (data) {
                    var payments = data[2];
                    payment_summary = data[1];
                    var final_total = data[0];

                    self.gui.close_popup();
                    self.gui.show_screen('payment_receipt', {
                        payment_summary: payment_summary,
                        final_total: final_total,
                        is_current_session: is_current_session,
                        payments: payments,
                        smry_payment: smry_payment,
                    });
                });
            } else {
                if (pay_st_date == false) {
                    // alert("Please fill Start Date.")
                    $('#dt_strt').show()
                    setTimeout(function () {
                        $('#dt_strt').hide()
                    }, 3000);
                    return
                } else if (pay_ed_date == false) {
                    // alert("Please fill End Date.")
                    $('#dt_end').show()
                    setTimeout(function () {
                        $('#dt_end').hide()
                    }, 3000);
                    return
                } else {

                    rpc.query({
                        model: 'pos.report.payment',
                        method: 'get_crnt_ssn_payment_pos_order',
                        args: [1, smry_payment, cashier.id, curr_session, is_current_session, pay_st_date, pay_ed_date],
                    }).then(function (data) {
                        var payments = data[2];
                        payment_summary = data[1];
                        var final_total = data[0];

                        self.gui.close_popup();
                        self.gui.show_screen('payment_receipt', {
                            payment_summary: payment_summary,
                            final_total: final_total,
                            is_current_session: is_current_session,
                            payments: payments,
                            start_date_pay: pay_st_date,
                            end_date_pay: pay_ed_date,
                            smry_payment: smry_payment,
                        });
                    });
                    return
                }

            }
        },
    });

    gui.define_popup({
        name: 'pos_payment_report_widget',
        widget: PopupPaymentWidget
    });

    var PaymentReceiptWidget = screens.ScreenWidget.extend({
        template: 'PaymentReceiptWidget',

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
        },

        show: function () {
            this._super();
            var self = this;
            this.payment_render_reciept();
        },


        get_payment_summery: function () {
            return this.gui.get_current_screen_param('payment_summary');
        },

        get_payment_st_date: function () {
            var st_date1 = this.gui.get_current_screen_param('start_date_pay')
            var st_date = st_date1.split("-")

            var st_date_d = st_date[2];
            var st_date_m = st_date[1];
            var st_date_y = st_date[0];
            var full_st_date = st_date_d + '-' + st_date_m + '-' + st_date_y
            return full_st_date;
        },
        get_payment_ed_date: function () {
            var ed_date = this.gui.get_current_screen_param('end_date_pay').split("-")

            var ed_date_d = ed_date[2];
            var ed_date_m = ed_date[1];
            var ed_date_y = ed_date[0];
            var full_ed_date = ed_date_d + '-' + ed_date_m + '-' + ed_date_y
            return full_ed_date;
        },

        get_payment_st_month: function () {
            var st_date = this.gui.get_current_screen_param('start_date_pay').split("-")

            var monthNames = ["",
                "January", "February", "March",
                "April", "May", "June", "July",
                "August", "September", "October",
                "November", "December"
            ];

            var st_date_m_index = st_date[1];
            var st_date_split = st_date_m_index.split('')

            if (st_date_split[0] > '0') {
                st_date_m_index = st_date_m_index
            } else {
                st_date_m_index = st_date_m_index.split('')[1]
            }
            var st_date_y = st_date[0];

            return monthNames[st_date_m_index] + '-' + st_date_y;
        },
        get_payment_ed_month: function () {
            var ed_date = this.gui.get_current_screen_param('end_date_pay').split("-")

            var monthNames = ["",
                "January", "February", "March",
                "April", "May", "June", "July",
                "August", "September", "October",
                "November", "December"
            ];

            var ed_date_m_index = ed_date[1];

            var ed_date_split = ed_date_m_index.split('')
            if (ed_date_split[0] > '0') {
                ed_date_m_index = ed_date_m_index
            } else {
                ed_date_m_index = ed_date_m_index.split('')[1]
            }
            var ed_date_y = ed_date[0];

            return monthNames[ed_date_m_index] + '-' + ed_date_y;
        },

        get_payment_final_total: function () {
            return this.gui.get_current_screen_param('final_total');
        },

        get_payment_receipt_render_env: function () {
            var self = this;
            var is_current_session = this.gui.get_current_screen_param('is_current_session')
            if (is_current_session == true) {
                return {
                    widget: this,
                    pos: this.pos,
                    payments: this.gui.get_current_screen_param('payments'),
                    is_current_session: is_current_session,
                    pay_summary: this.get_payment_summery(),
                    final_total: this.get_payment_final_total(),
                    date_pay: (new Date()).toLocaleString(),
                    smry_payment: this.gui.get_current_screen_param('smry_payment'),
                };

            } else {
                return {
                    widget: this,
                    pos: this.pos,
                    is_current_session: is_current_session,
                    pay_summary: this.get_payment_summery(),
                    payments: this.gui.get_current_screen_param('payments'),
                    final_total: this.get_payment_final_total(),
                    smry_payment: this.gui.get_current_screen_param('smry_payment'),
                    st_date_pay: this.get_payment_st_date(),
                    ed_date_pay: this.get_payment_ed_date(),
                    st_month_pay: this.get_payment_st_month(),
                    ed_month_pay: this.get_payment_ed_month(),
                    date_pay: (new Date()).toLocaleString(),
                };
            }

        },
        payment_render_reciept: function () {
            this.$('.pos-payment-receipt-container').html(QWeb.render('PosPaymentSummaryReceipt', this.get_payment_receipt_render_env()));
        },

        print_xml_payment: function () {
            var receipt = QWeb.render('PosOrderSummaryReceipt', this.get_order_receipt_render_env());
            this.pos.proxy.print_receipt(receipt);
        },

        print_web_payment: function () {
            window.print();
        },

        print_payment: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {

                this.print_web_payment();
            } else {
                this.print_xml_payment();
            }
        },

        renderElement: function () {
            var self = this;
            this._super();

            this.$('.next').click(function () {
                self.gui.show_screen('products');
            });

            this.$('.button.print-payment').click(function () {
                self.print_payment();
            });

        },


    });
    gui.define_screen({name: 'payment_receipt', widget: PaymentReceiptWidget});


    /*#################################################### Payment Summary End ################################################################*/

    /*#################################################### Order Summary ################################################################*/

    var ReportOrderButtonWidget = screens.ActionButtonWidget.extend({
        template: 'ReportOrderButtonWidget',

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
        },

        button_click: function () {
            var self = this;

            self.gui.show_popup('pos_order_report_widget')

        },
        renderElement: function () {
            var self = this;
            this._super();
        },

    });

    screens.define_action_button({
        'name': 'Pos Order Summary Widget',
        'widget': ReportOrderButtonWidget,
        'condition': function () {
            return true;
        },
    });

    var PopupOrderWidget = popups.extend({
        template: 'PopupOrderWidget',

        init: function (parent, args) {
            var self = this;
            this._super(parent, args);
        },

        events: {
            'click .button.print-order': 'print_order',
            'click .button.cancel-order': 'close_popup_o',
        },

        close_popup_o: function () {
            this.gui.close_popup();
        },

        renderElement: function () {
            var self = this;
            this._super();
            $('#ordr_dt_strt').hide();
            $('#ordr_dt_end').hide();

            $('#ordr_crnt_ssn').click(function () {
                if ($('#ordr_crnt_ssn').is(':checked')) {
                    $('#order_st').hide();
                    $('#order_end').hide();
                } else {
                    $('#order_st').show();
                    $('#order_end').show();
                }
            });

        },

        print_order: function () {
            var self = this;
            var ord_st_date = this.$('#ord_st_date').val()
            var ord_end_date = this.$('#ord_end_date').val()
            var ord_state = this.$('#ord_state').val()
            var order = this.pos.get_order();
            var summery_order = [];
            var curr_session = self.pos.config.current_session_id[0];
            var order_current_session = $('#ordr_crnt_ssn').is(':checked')
            $('#ordr_dt_strt').hide();
            $('#ordr_dt_end').hide();
            if (order_current_session == true) {
                rpc.query({
                    model: 'pos.order',
                    method: 'update_order_summery',
                    args: [order['sequence_number'], ord_st_date, ord_end_date, ord_state, curr_session, order_current_session],
                }).then(function (output_summery) {
                    summery_order = output_summery;
                    self.save_summery_details(output_summery, ord_st_date, ord_end_date, order_current_session);

                });
            } else {
                if (ord_st_date == false) {
                    $('#ordr_dt_strt').show()
                    setTimeout(function () {
                        $('#ordr_dt_strt').hide()
                    }, 3000);
                    return
                } else if (ord_end_date == false) {
                    $('#ordr_dt_end').show()
                    setTimeout(function () {
                        $('#ordr_dt_end').hide()
                    }, 3000);
                    return
                } else {
                    rpc.query({
                        model: 'pos.order',
                        method: 'update_order_summery',
                        args: [order['sequence_number'], ord_st_date, ord_end_date, ord_state, curr_session, order_current_session],
                    }).then(function (output_summery) {
                        summery_order = output_summery;
                        self.save_summery_details(output_summery, ord_st_date, ord_end_date, order_current_session);

                    });
                }
            }

        },

        save_summery_details: function (output_summery, ord_st_date, ord_end_date, order_current_session) {
            var self = this;
            this.gui.close_popup();
            this.gui.show_screen('order_summery_receipt', {
                output_summery: output_summery,
                ord_start_dt: ord_st_date,
                ord_end_dt: ord_end_date,
                order_current_session: order_current_session
            });
        },

    });

    gui.define_popup({
        name: 'pos_order_report_widget',
        widget: PopupOrderWidget
    });


    var OrderReceiptWidget = screens.ScreenWidget.extend({
        template: 'OrderReceiptWidget',

        init: function (parent, args) {
            this._super(parent, args);
            this.options = {};
        },

        show: function (options) {
            var self = this;
            this._super(options);
            this.order_render_reciept();
        },

        get_summery: function () {
            return this.gui.get_current_screen_param('output_summery');
        },

        get_order_st_date: function () {
            return this.gui.get_current_screen_param('ord_start_dt');

        },
        get_order_ed_date: function () {
            return this.gui.get_current_screen_param('ord_end_dt');

        },

        get_order_receipt_render_env: function () {
            // var order = this.pos.get_order();
            return {
                widget: this,
                pos: this.pos,
                // order: order,
                order_current_session: this.gui.get_current_screen_param('order_current_session'),
                summery: this.get_summery(),
                st_date: this.get_order_st_date(),
                ed_date: this.get_order_ed_date(),
                date_o: (new Date()).toLocaleString(),
                //receipt: order.export_for_printing(),
                //orderlines: order.get_orderlines(),
                //paymentlines: order.get_paymentlines(),
            };
        },
        order_render_reciept: function () {
            this.$('.pos-order-receipt-container').html(QWeb.render('PosOrderSummaryReceipt', this.get_order_receipt_render_env()));
        },

        print_xml_order: function () {
            var receipt = QWeb.render('PosOrderSummaryReceipt', this.get_order_receipt_render_env());
            this.pos.proxy.print_receipt(receipt);
        },

        print_web_order: function () {
            window.print();
        },

        print_order: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {

                this.print_web_order();
            } else {
                this.print_xml_order();
            }
        },

        renderElement: function () {
            var self = this;
            this._super();

            this.$('.next').click(function () {
                self.gui.show_screen('products');
            });

            this.$('.button.print-order').click(function () {
                self.print_order();
            });

        },

    });

    gui.define_screen({name: 'order_summery_receipt', widget: OrderReceiptWidget});


    /*#################################################### Order Summary End ################################################################*/


    /*#################################################### Product Summary ################################################################*/

    var ReportProductButtonWidget = screens.ActionButtonWidget.extend({
        template: 'ReportProductButtonWidget',

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
        },

        button_click: function () {
            var self = this;
            this._super();

            self.gui.show_popup('pos_product_report_widget')

        },

        renderElement: function () {
            var self = this;
            this._super();
        },

    });

    screens.define_action_button({
        'name': 'Pos Product Summary Widget',
        'widget': ReportProductButtonWidget,
        'condition': function () {
            return true;
        },
    });

    var PopupProductWidget = popups.extend({
        template: 'PopupProductWidget',

        init: function (parent, args) {
            var self = this;
            this._super(parent, args);
        },

        events: {
            'click .button.print-product': 'print_product',
            'click .button.cancel-product': 'close_popup_p',
        },

        close_popup_p: function () {
            this.gui.close_popup();
        },

        renderElement: function () {
            var self = this;
            this._super();
            $('#prod_dt_strt').hide();
            $('#prod_dt_end').hide();

            $('#prod_crnt_ssn').click(function () {
                if ($('#prod_crnt_ssn').is(':checked')) {
                    $('#prod_st_dt').hide();
                    $('#prod_end_dt').hide();
                } else {
                    $('#prod_st_dt').show();
                    $('#prod_end_dt').show();
                }
            });

        },

        print_product: function () {
            var self = this;
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
        },

        save_product_summery_details: function (output_summery_product, pro_st_date, pro_ed_date, prod_current_session) {
            var self = this;
            this.gui.close_popup();
            this.gui.show_screen('product_summery_receipt', {
                output_summery_product: output_summery_product,
                pro_st_date: pro_st_date,
                pro_ed_date: pro_ed_date,
                prod_current_session: prod_current_session
            });
        },

    });

    gui.define_popup({
        name: 'pos_product_report_widget',
        widget: PopupProductWidget
    });

    var ProductReceiptWidget = screens.ScreenWidget.extend({
        template: 'ProductReceiptWidget',

        init: function (parent, args) {
            this._super(parent, args);
            this.options = {};


        },

        show: function (options) {

            var self = this;
            this._super(options);
            this.product_render_reciept();
        },

        get_pro_summery: function () {
            return this.gui.get_current_screen_param('output_summery_product');
        },

        get_product_st_date: function () {
            return this.gui.get_current_screen_param('pro_st_date');

        },
        get_product_ed_date: function () {
            return this.gui.get_current_screen_param('pro_ed_date');

        },

        get_product_receipt_render_env: function () {
            // var order = this.pos.get_order();
            return {
                widget: this,
                pos: this.pos,
                // order: order,
                prod_current_session: this.gui.get_current_screen_param('prod_current_session'),
                p_summery: this.get_pro_summery(),
                p_st_date: this.get_product_st_date(),
                p_ed_date: this.get_product_ed_date(),
                date_p: (new Date()).toLocaleString(),
                //receipt: order.export_for_printing(),
                //orderlines: order.get_orderlines(),
                //paymentlines: order.get_paymentlines(),
            };
        },
        product_render_reciept: function () {
            this.$('.pos-product-receipt-container').html(QWeb.render('PosProductSummaryReceipt', this.get_product_receipt_render_env()));
        },

        print_xml_product: function () {
            var receipt = QWeb.render('PosProductSummaryReceipt', this.get_product_receipt_render_env());
            this.pos.proxy.print_receipt(receipt);
        },

        print_web_product: function () {
            window.print();
        },

        print_product: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {

                this.print_web_product();
            } else {
                this.print_xml_product();
            }
        },

        renderElement: function () {
            var self = this;
            this._super();

            this.$('.next').click(function () {
                self.gui.show_screen('products');
            });

            this.$('.button.print-product').click(function () {
                self.print_product();
            });

        },


    });



    var ProducttReceipttWidget = screens.ScreenWidget.extend({
        template: 'ProducttReceipttWidget',

        init: function (parent, args) {
            this._super(parent, args);
            this.options = {};


        },

        show: function (options) {

            var self = this;
            this._super(options);
            this.product_render_reciept();
        },

        get_pro_summery: function () {
            return this.gui.get_current_screen_param('output_summery_product');
        },

        get_product_st_date: function () {
            return this.gui.get_current_screen_param('pro_st_date');

        },
        get_product_ed_date: function () {
            return this.gui.get_current_screen_param('pro_ed_date');

        },

        get_product_receipt_render_env: function () {
            // var order = this.pos.get_order();
            return {
                widget: this,
                pos: this.pos,
                // order: order,
                prod_current_session: this.gui.get_current_screen_param('prod_current_session'),
                p_summery: this.get_pro_summery(),
                p_st_date: this.get_product_st_date(),
                p_ed_date: this.get_product_ed_date(),
                date_p: (new Date()).toLocaleString(),
                //receipt: order.export_for_printing(),
                //orderlines: order.get_orderlines(),
                //paymentlines: order.get_paymentlines(),
            };
        },
        product_render_reciept: function () {
            this.$('.pos-product-receipt-container').html(QWeb.render('PosProductSummaryReceipt', this.get_product_receipt_render_env()));
        },

        print_xml_product: function () {
            var receipt = QWeb.render('PosProductSummaryReceipt', this.get_product_receipt_render_env());
            this.pos.proxy.print_receipt(receipt);
        },

        print_web_product: function () {
            window.print();
        },

        print_product: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {

                this.print_web_product();
            } else {
                this.print_xml_product();
            }
        },

        renderElement: function () {
            var self = this;
            this._super();

            this.$('.nextt').click(function () {
                // self.gui.show_screen('products');
            //     var self = this;
            //     var id = self.pos.config.current_session_id[0];

            //     rpc.query({
            //     model: 'pos.session',
            //     method: 'action_pos_session_closing_control',
            //     args: [id]
            // }).then(function (result) {
            //     $('.session').trigger('click');
            // }, function (err, event) {
            //     event.preventDefault();
            //     var err_msg = 'Please verify the details given or Check the Internet Connection./n';
            //     if (err.data.message)
            //         err_msg = err.data.message;
            //     self.gui.show_popup('alert', {
            //         'title': _t('Odoo Warning'),
            //         'body': _t(err_msg),
            //     });
            // });
            // var cashier = self.pos.user || false;
            // if(cashier && cashier.login_with_pos_screen){
            //     framework.redirect('/web/session/logout');
            // } else{
            self.pos.gui.close();
            // }
            
            // this.gui.close_popup();
            });

            this.$('.button.print-product').click(function () {
                self.print_product();
            });

        },


    });
    gui.define_screen({name: 'product_summery_receipt', widget: ProductReceiptWidget});
    gui.define_screen({name: 'product_summery_receipt2', widget: ProducttReceipttWidget});

    /*#################################################### product Summary End ################################################################*/

    /*######################################################## Category Summary ################################################*/


    var ReportCategoryButtonWidget = screens.ActionButtonWidget.extend({
        template: 'ReportCategoryButtonWidget',

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
        },

        button_click: function () {
            var self = this;
            this._super();
            self.gui.show_popup('pos_category_report_widget')
        },

        renderElement: function () {
            var self = this;
            this._super();
        },

    });

    screens.define_action_button({
        'name': 'Pos Category Summary Widget',
        'widget': ReportCategoryButtonWidget,
        'condition': function () {
            return true;
        },
    });

    var PopupCategoryWidget = popups.extend({
        template: 'PopupCategoryWidget',

        init: function (parent, args) {
            var self = this;
            this._super(parent, args);
        },

        renderElement: function () {
            var self = this;
            this._super();
            $('#categ_dt_strt').hide();
            $('#categ_dt_end').hide();

            $('#categ_crnt_ssn').click(function () {
                if ($('#categ_crnt_ssn').is(':checked')) {
                    $('#ct_st_dt').hide();
                    $('#ct_end_dt').hide();
                } else {
                    $('#ct_st_dt').show();
                    $('#ct_end_dt').show();
                }
            });
            this.$('.print').click(function () {
                self.render_category_summary();
            });
        },

        render_category_summary: function () {
            var self = this;
            var categ_st_date = this.$('#categ_st_date').val()
            var categ_ed_date = this.$('#categ_ed_date').val()
            // var order = this.pos.get_order();
            var category_summary = [];
            var curr_session = self.pos.config.current_session_id[0];
            var categ_current_session = $('#categ_crnt_ssn').is(':checked')
            $('#categ_dt_strt').hide();
            $('#categ_dt_end').hide();

            if (categ_current_session == true) {
                rpc.query({
                    model: 'pos.report.category',
                    method: 'get_category_pos_order',
                    args: [self.pos.order_sequence, categ_st_date, categ_ed_date, curr_session, categ_current_session],
                }).then(function (data) {
                    category_summary = data;
                    var make_total = [];
                    var final_total = null;

                    for (var i = 0; i < category_summary.length; i++) {
                        make_total.push(category_summary[i].sum)
                        final_total = make_total.reduce(function (acc, val) {
                            return acc + val;
                        });
                    }
                    self.gui.close_popup();
                    self.gui.show_screen('category_receipt', {
                        category_summary: category_summary,
                        start_date_categ: categ_st_date,
                        end_date_categ: categ_ed_date,
                        final_total: final_total,
                        categ_current_session: categ_current_session,
                    });
                });
            } else {
                if (categ_st_date == false) {
                    $('#categ_dt_strt').show()
                    setTimeout(function () {
                        $('#categ_dt_strt').hide()
                    }, 3000);
                    return
                } else if (categ_ed_date == false) {
                    $('#categ_dt_end').show()
                    setTimeout(function () {
                        $('#categ_dt_end').hide()
                    }, 3000);
                    return
                } else {
                    rpc.query({
                        model: 'pos.report.category',
                        method: 'get_category_pos_order',
                        args: [self.pos.order_sequence, categ_st_date, categ_ed_date, curr_session, categ_current_session],
                    }).then(function (data) {
                        category_summary = data;
                        var make_total = [];
                        var final_total = null;

                        for (var i = 0; i < category_summary.length; i++) {
                            make_total.push(category_summary[i].sum)
                            final_total = make_total.reduce(function (acc, val) {
                                return acc + val;
                            });
                        }
                        self.gui.close_popup();
                        self.gui.show_screen('category_receipt', {
                            category_summary: category_summary,
                            start_date_categ: categ_st_date,
                            end_date_categ: categ_ed_date,
                            final_total: final_total,
                            categ_current_session: categ_current_session,
                        });
                    });
                }
            }
        },


    });

    gui.define_popup({
        name: 'pos_category_report_widget',
        widget: PopupCategoryWidget
    });

    var CategoryReceiptWidget = screens.ScreenWidget.extend({
        template: 'CategoryReceiptWidget',

        show: function () {
            this._super();
            var self = this;
            this.category_render_reciept();
        },


        get_category_summery: function () {
            return this.gui.get_current_screen_param('category_summary');
        },

        get_category_st_date: function () {
            var st_date = this.gui.get_current_screen_param('start_date_categ').split("-")

            var st_date_d = st_date[2];
            var st_date_m = st_date[1];
            var st_date_y = st_date[0];
            var full_st_date = st_date_d + '-' + st_date_m + '-' + st_date_y
            return full_st_date;
        },
        get_category_ed_date: function () {
            var ed_date = this.gui.get_current_screen_param('end_date_categ').split("-")

            var ed_date_d = ed_date[2];
            var ed_date_m = ed_date[1];
            var ed_date_y = ed_date[0];
            var full_ed_date = ed_date_d + '-' + ed_date_m + '-' + ed_date_y
            return full_ed_date;
        },

        get_category_st_month: function () {
            var st_date = this.gui.get_current_screen_param('start_date_categ').split("-")

            var monthNames = ["",
                "January", "February", "March",
                "April", "May", "June", "July",
                "August", "September", "October",
                "November", "December"
            ];

            var st_date_m_index = st_date[1];
            var st_date_split = st_date_m_index.split('')

            if (st_date_split[0] > '0') {
                st_date_m_index = st_date_m_index
            } else {
                st_date_m_index = st_date_m_index.split('')[1]
            }
            var st_date_y = st_date[0];

            return monthNames[st_date_m_index] + '-' + st_date_y;
        },
        get_category_ed_month: function () {
            var ed_date = this.gui.get_current_screen_param('end_date_categ').split("-")

            var monthNames = ["",
                "January", "February", "March",
                "April", "May", "June", "July",
                "August", "September", "October",
                "November", "December"
            ];

            var ed_date_m_index = ed_date[1];

            var ed_date_split = ed_date_m_index.split('')
            if (ed_date_split[0] > '0') {
                ed_date_m_index = ed_date_m_index
            } else {
                ed_date_m_index = ed_date_m_index.split('')[1]
            }
            var ed_date_y = ed_date[0];

            return monthNames[ed_date_m_index] + '-' + ed_date_y;
        },

        get_category_final_total: function () {
            return this.gui.get_current_screen_param('final_total');
        },

        get_category_receipt_render_env: function () {
            var self = this;
            // var order = this.pos.get_order();
            var categ_current_session = this.gui.get_current_screen_param('categ_current_session');
            if (categ_current_session == true) {
                return {
                    widget: this,
                    pos: this.pos,
                    categ_current_session: categ_current_session,
                    cate_summary: this.get_category_summery(),
                    final_total: this.get_category_final_total(),
                    date_c: (new Date()).toLocaleString()
                };
            } else {
                return {
                    widget: this,
                    pos: this.pos,
                    categ_current_session: categ_current_session,
                    cate_summary: this.get_category_summery(),
                    st_date_categ: this.get_category_st_date(),
                    ed_date_categ: this.get_category_ed_date(),
                    st_month_categ: this.get_category_st_month(),
                    ed_month_categ: this.get_category_ed_month(),
                    final_total: this.get_category_final_total(),
                    date_c: (new Date()).toLocaleString()
                };
            }

        },
        category_render_reciept: function () {
            this.$('.pos-category-receipt-container').html(QWeb.render('PosCategorySummaryReceipt', this.get_category_receipt_render_env()));
        },

        print_xml_categ: function () {
            var receipt = QWeb.render('PosCategorySummaryReceipt', this.get_category_receipt_render_env());
            this.pos.proxy.print_receipt(receipt);
        },

        print_web_categ: function () {
            window.print();
        },

        print_categ: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) {

                this.print_web_categ();
            } else {
                this.print_xml_categ();
            }
        },

        renderElement: function () {
            var self = this;
            this._super();

            this.$('.next').click(function () {
                self.gui.show_screen('products');
            });

            this.$('.button.print-categ').click(function () {
                self.print_categ();
            });

        },

    });
    gui.define_screen({name: 'category_receipt', widget: CategoryReceiptWidget});


    //######################################################## Location Summery ################################################################

    var ReportLocationButtonWidget = screens.ActionButtonWidget.extend({
        template: 'ReportLocationButtonWidget',

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
        },

        button_click: function () {
            var self = this;
            this._super();
            self.gui.show_popup('pos_location_report_widget')
        },

        renderElement: function () {
            var self = this;
            this._super();
        },

    });

    screens.define_action_button({
        'name': 'Pos Location Summary Widget',
        'widget': ReportLocationButtonWidget,

    });

    var PopupLocationWidget = popups.extend({
        template: 'PopupLocationWidget',

        init: function (parent, args) {
            var self = this;
            this._super(parent, args);
        },

        events: {
            'click .button.print-location': 'print_location',
            'click .button.cancel-loc': 'close_popup_l',
        },

        close_popup_l: function () {
            this.gui.close_popup();
        },

        renderElement: function () {
            var self = this;
            this._super();
            $('#select_ssn').hide();
            $('#select_loc').hide();
        },

        print_location: function () {
            var self = this;
            var select_session = $('.select_session_id').val();
            var location = $('.summery_location_id').val();
            var tab1 = $('#tab1').is(':checked');
            $('#select_ssn').hide();
            $('#select_loc').hide();
            var ram = false;
            if (tab1) {
                ram = true;
                if (select_session) {
                    rpc.query({
                        model: 'pos.order.location',
                        method: 'get_audit_by_session',
                        args: [select_session],
                    }).then(function (output_summery_location) {
                        self.save_location_summery_details(output_summery_location, ram);
                    });
                } else {
                    $('#select_ssn').show();
                    setTimeout(function () {
                        $('#select_ssn').hide()
                    }, 3000);
                    $('#tab1').prop('checked', true);
                }

            } else {
                if (location) {
                    rpc.query({
                        model: 'pos.order.location',
                        method: 'get_audit_by_location',
                        args: [location],
                    }).then(function (output_summery_location) {
                        self.save_location_summery_details(output_summery_location, ram);
                    });
                } else {
                    $('#select_loc').show();
                    setTimeout(function () {
                        $('#select_loc').hide()
                    }, 3000);
                    $('#tab2').prop('checked', true);
                }
            }
        },

        save_location_summery_details: function (output_summery_location, ram) {
            var self = this;
            this.gui.close_popup();
            this.gui.show_screen('loc_summery_receipt', {output_summery_location: output_summery_location, ssn: ram});
        },

    });

    gui.define_popup({
        name: 'pos_location_report_widget',
        widget: PopupLocationWidget
    });

    var LocationReceiptWidget = screens.ScreenWidget.extend({
        template: 'LocationReceiptWidget',

        init: function (parent, args) {
            this._super(parent, args);
            this.options = {};
        },

        show: function (options) {

            var self = this;
            this._super(options);
            this.location_render_reciept();
        },

        get_loc_summery: function () {
            return this.gui.get_current_screen_param('output_summery_location');
        },

        get_location_receipt_render_env: function () {
            return {
                widget: this,
                pos: this.pos,
                ssn: this.gui.get_current_screen_param('ssn'),
                loc_summery: this.get_loc_summery(),
                date: (new Date()).toLocaleString()

            };
        },
        location_render_reciept: function () {
            this.$('.pos-location-receipt-container').html(QWeb.render('PosLocationSummaryReceipt', this.get_location_receipt_render_env()));
        },

        print_xml: function () {
            var receipt = QWeb.render('PosLocationSummaryReceipt', this.get_location_receipt_render_env());
            this.pos.proxy.print_receipt(receipt);
        },

        print_web: function () {
            window.print();
            this.pos.get_order()._printed = true;
        },

        print: function () {
            var self = this;
            if (!this.pos.config.iface_print_via_proxy) { // browser (html) printing

                this.print_web();
            } else {
                this.print_xml();
            }
        },

        renderElement: function () {
            var self = this;
            this._super();

            this.$('.next').click(function () {
                self.gui.show_screen('products');
            });

            this.$('.button.print-loc').click(function () {
                self.print();
            });

        },


    });
    gui.define_screen({name: 'loc_summery_receipt', widget: LocationReceiptWidget});

    //######################################################## Location Summery End ################################################################


});
