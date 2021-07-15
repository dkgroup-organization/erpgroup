odoo.define('skit_pos_session_report.pos_session_report', function(require) {
	"use strict";		
var screens = require('point_of_sale.screens');
var OrderWidget = screens.OrderWidget;
var gui = require('point_of_sale.gui');
var PopupWidget = require('point_of_sale.popups');
var models = require('point_of_sale.models');
var utils = require('web.utils');

	var SessionReportButton = screens.ActionButtonWidget.extend({
		template : 'SessionReport',		
		button_click : function() {
			var self = this;
	    	var id = self.pos.pos_session.id;
	    	self.chrome.do_action('skit_pos_session_report.pos_session_report',
	    	   {additional_context:{active_ids:[id],}
	    	});
		},		
	});
	
	screens.define_action_button({
		'name' : 'sessionreport',		
		'widget' : SessionReportButton,
	});
	

});