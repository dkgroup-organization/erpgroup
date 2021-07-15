# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################


from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home, ensure_db


class Home(Home):
    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, **kw):
        res = super(Home, self).web_login(redirect, **kw)
        if request.params['login_success']:
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            users = request.env['res.users'].browse([uid])
            if users.login_with_pos_screen:
                pos_session = request.env['pos.session'].sudo().search(
                    [('config_id', '=', users.default_pos.id), ('state', '=', 'opened')])
                if pos_session:
                    pos_session.action_pos_session_closing_control()
                    session_id = users.default_pos.open_session_cb()
                    pos_session = request.env['pos.session'].sudo().search(
                        [('config_id', '=', users.default_pos.id), ('state', '=', 'opening_control')])

                    pos_session.action_pos_session_open()
                    return http.redirect_with_hash('/pos/web')
                else:
                    session_id = users.default_pos.open_session_cb()
                    pos_session = request.env['pos.session'].sudo().search(
                        [('config_id', '=', users.default_pos.id), ('state', '=', 'opening_control')])

                    pos_session.action_pos_session_open()
                    return http.redirect_with_hash('/pos/web')
            else:
                return res
        else:
            return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: