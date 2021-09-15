# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import babel.messages.pofile
import base64
import copy
import datetime
import functools
import glob
import hashlib
import io
import itertools
import jinja2
import json
import logging
import operator
import os
import re
import sys
import tempfile
import time

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from collections import OrderedDict, defaultdict, Counter
from werkzeug.urls import url_decode, iri_to_uri
from lxml import etree
import unicodedata


import odoo
import odoo.modules.registry
from odoo.api import call_kw, Environment
from odoo.modules import get_module_path, get_resource_path
from odoo.tools import image_process, topological_sort, html_escape, pycompat, ustr, apply_inheritance_specs, lazy_property, float_repr
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.translate import _
from odoo.tools.misc import str2bool, xlsxwriter, file_open
from odoo.tools.safe_eval import safe_eval
from odoo import http, tools
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception, Response
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.models import check_method_name
from odoo.service import db, security

_logger = logging.getLogger(__name__)

class Home(http.Controller):

    @http.route('/', type='http', auth="none", cors='*')
    def index(self, s_action=None, db=None, **kw):
        return http.local_redirect('/web', query=request.params, keep_hash=True)

    # ideally, this route should be `auth="user"` but that don't work in non-monodb mode.
#     @http.route('/web', type='http', auth="none", cors='*')
#     def web_client(self, s_action=None, **kw):
#         ensure_db()
#         if not request.session.uid:
#             return werkzeug.utils.redirect('/web/login', 303)
#         if kw.get('redirect'):
#             return werkzeug.utils.redirect(kw.get('redirect'), 303)

#         request.uid = request.session.uid
#         try:
#             context = request.env['ir.http'].webclient_rendering_context()
#             response = request.render('web.webclient_bootstrap', qcontext=context)
#             response.headers['X-Frame-Options'] = 'DENY'
#             return response
#         except AccessError:
#             return werkzeug.utils.redirect('/web/login?error=access')

    @http.route('/web/webclient/load_menus/<string:unique>', type='http', auth='user', methods=['GET'], cors='*' ) #cors Added to deblock third party
    def web_load_menus(self, unique):
        """
        Loads the menus for the webclient
        :param unique: this parameters is not used, but mandatory: it is used by the HTTP stack to make a unique request
        :return: the menus (including the images in Base64)
        """
        menus = request.env["ir.ui.menu"].load_menus(request.session.debug)
        body = json.dumps(menus, default=ustr)
        response = request.make_response(body, [
            # this method must specify a content-type application/json instead of using the default text/html set because
            # the type of the route is set to HTTP, but the rpc is made with a get and expects JSON
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'public, max-age=' + str(CONTENT_MAXAGE)),
        ])
        return response

    @http.route('/web/dbredirect', type='http', auth="none", cors='*')
    def web_db_redirect(self, redirect='/', **kw):
        ensure_db()
        return werkzeug.utils.redirect(redirect, 303)

    def _login_redirect(self, uid, redirect=None):
        return redirect if redirect else '/web'

    @http.route('/web/login', type='http', auth="none", cors='*')
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
                request.params['login_success'] = True
                return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route('/web/become', type='http', auth='user', sitemap=False)
    def switch_to_admin(self):
        uid = request.env.user.id
        if request.env.user._is_system():
            uid = request.session.uid = odoo.SUPERUSER_ID
            request.env['res.users']._invalidate_session_cache()
            request.session.session_token = security.compute_session_token(request.session, request.env)

        return http.local_redirect(self._login_redirect(uid), keep_hash=True)

    
class WebClient(http.Controller):

    @http.route('/web/webclient/csslist', type='json', auth="none", cors='*')
    def csslist(self, mods=None):
        return manifest_list('css', mods=mods)

    @http.route('/web/webclient/jslist', type='json', auth="none", cors='*')
    def jslist(self, mods=None):
        return manifest_list('js', mods=mods)

    @http.route('/web/webclient/locale/<string:lang>', type='http', auth="none")
    def load_locale(self, lang):
        magic_file_finding = [lang.replace("_", '-').lower(), lang.split('_')[0]]
        for code in magic_file_finding:
            try:
                return http.Response(
                    werkzeug.wsgi.wrap_file(
                        request.httprequest.environ,
                        file_open('web/static/lib/moment/locale/%s.js' % code, 'rb')
                    ),
                    content_type='application/javascript; charset=utf-8',
                    headers=[('Cache-Control', 'max-age=%s' % http.STATIC_CACHE)],
                    direct_passthrough=True,
                )
            except IOError:
                _logger.debug("No moment locale for code %s", code)

        return request.make_response("", headers=[
            ('Content-Type', 'application/javascript'),
            ('Cache-Control', 'max-age=%s' % http.STATIC_CACHE),
        ])

    @http.route('/web/webclient/qweb/<string:unique>', type='http', auth="none", cors="*")
    def qweb(self, unique, mods=None, db=None):
        content = HomeStaticTemplateHelpers.get_qweb_templates(mods, db, debug=request.session.debug)

        return request.make_response(content, [
                ('Content-Type', 'text/xml'),
                ('Cache-Control','public, max-age=' + str(CONTENT_MAXAGE))
            ])

    @http.route('/web/webclient/bootstrap_translations', type='json', auth="none")
    def bootstrap_translations(self, mods):
        """ Load local translations from *.po files, as a temporary solution
            until we have established a valid session. This is meant only
            for translating the login page and db management chrome, using
            the browser's language. """
        # For performance reasons we only load a single translation, so for
        # sub-languages (that should only be partially translated) we load the
        # main language PO instead - that should be enough for the login screen.
        context = dict(request.context)
        request.session._fix_lang(context)
        lang = context['lang'].split('_')[0]

        translations_per_module = {}
        for addon_name in mods:
            if http.addons_manifest[addon_name].get('bootstrap'):
                addons_path = http.addons_manifest[addon_name]['addons_path']
                f_name = os.path.join(addons_path, addon_name, "i18n", lang + ".po")
                if not os.path.exists(f_name):
                    continue
                translations_per_module[addon_name] = {'messages': _local_web_translations(f_name)}

        return {"modules": translations_per_module,
                "lang_parameters": None}

    @http.route('/web/webclient/translations/<string:unique>', type='http', auth="public")
    def translations(self, unique, mods=None, lang=None):
        """
        Load the translations for the specified language and modules

        :param unique: this parameters is not used, but mandatory: it is used by the HTTP stack to make a unique request
        :param mods: the modules, a comma separated list
        :param lang: the language of the user
        :return:
        """
        request.disable_db = False

        if mods:
            mods = mods.split(',')
        translations_per_module, lang_params = request.env["ir.translation"].get_translations_for_webclient(mods, lang)

        body = json.dumps({
            'lang': lang,
            'lang_parameters': lang_params,
            'modules': translations_per_module,
            'multi_lang': len(request.env['res.lang'].sudo().get_installed()) > 1,
        })
        response = request.make_response(body, [
            # this method must specify a content-type application/json instead of using the default text/html set because
            # the type of the route is set to HTTP, but the rpc is made with a get and expects JSON
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'public, max-age=' + str(CONTENT_MAXAGE)),
        ])
        return response

    @http.route('/web/webclient/version_info', type='json', auth="none")
    def version_info(self):
        return odoo.service.common.exp_version()

    @http.route('/web/tests', type='http', auth="user")
    def test_suite(self, mod=None, **kwargs):
        return request.render('web.qunit_suite')

    @http.route('/web/tests/mobile', type='http', auth="none")
    def test_mobile_suite(self, mod=None, **kwargs):
        return request.render('web.qunit_mobile_suite')

    @http.route('/web/benchmarks', type='http', auth="none")
    def benchmarks(self, mod=None, **kwargs):
        return request.render('web.benchmark_suite')

    
    
    
class Proxy(http.Controller):

    @http.route('/web/proxy/post/<path:path>', type='http', auth='user', methods=['GET'], cors='*', csrf=False)
    def post(self, path):
        """Effectively execute a POST request that was hooked through user login"""
        with request.session.load_request_data() as data:
            if not data:
                raise werkzeug.exceptions.BadRequest()
            from werkzeug.test import Client
            from werkzeug.wrappers import BaseResponse
            base_url = request.httprequest.base_url
            query_string = request.httprequest.query_string
            client = Client(request.httprequest.app, BaseResponse)
            headers = {'X-Openerp-Session-Id': request.session.sid}
            return client.post('/' + path, base_url=base_url, query_string=query_string,
                               headers=headers, data=data)
        
class Database(http.Controller):

    def _render_template(self, **d):
        d.setdefault('manage',True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("database_manager.html").render(d)

    @http.route('/web/database/selector', type='http', auth="none")
    def selector(self, **kw):
        request._cr = None
        return self._render_template(manage=False)

    @http.route('/web/database/manager', type='http', auth="none")
    def manager(self, **kw):
        request._cr = None
        return self._render_template()

    @http.route('/web/database/create', type='http', auth="none", methods=['POST'], csrf=False, cors='*')
    def create(self, master_pwd, name, lang, password, **post):
        try:
            if not re.match(DBNAME_PATTERN, name):
                raise Exception(_('Invalid database name. Only alphanumerical characters, underscore, hyphen and dot are allowed.'))
            # country code could be = "False" which is actually True in python
            country_code = post.get('country_code') or False
            dispatch_rpc('db', 'create_database', [master_pwd, name, bool(post.get('demo')), lang, password, post['login'], country_code, post['phone']])
            request.session.authenticate(name, post['login'], password)
            return http.local_redirect('/web/')
        except Exception as e:
            error = "Database creation error: %s" % (str(e) or repr(e))
        return self._render_template(error=error)

    @http.route('/web/database/duplicate', type='http', auth="none", methods=['POST'], csrf=False)
    def duplicate(self, master_pwd, name, new_name):
        try:
            if not re.match(DBNAME_PATTERN, new_name):
                raise Exception(_('Invalid database name. Only alphanumerical characters, underscore, hyphen and dot are allowed.'))
            dispatch_rpc('db', 'duplicate_database', [master_pwd, name, new_name])
            request._cr = None  # duplicating a database leads to an unusable cursor
            return http.local_redirect('/web/database/manager')
        except Exception as e:
            error = "Database duplication error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    @http.route('/web/database/drop', type='http', auth="none", methods=['POST'], csrf=False)
    def drop(self, master_pwd, name):
        try:
            dispatch_rpc('db','drop', [master_pwd, name])
            request._cr = None  # dropping a database leads to an unusable cursor
            return http.local_redirect('/web/database/manager')
        except Exception as e:
            error = "Database deletion error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    @http.route('/web/database/backup', type='http', auth="none", methods=['POST'], csrf=False)
    def backup(self, master_pwd, name, backup_format = 'zip'):
        try:
            odoo.service.db.check_super(master_pwd)
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            filename = "%s_%s.%s" % (name, ts, backup_format)
            headers = [
                ('Content-Type', 'application/octet-stream; charset=binary'),
                ('Content-Disposition', content_disposition(filename)),
            ]
            dump_stream = odoo.service.db.dump_db(name, None, backup_format)
            response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
            return response
        except Exception as e:
            _logger.exception('Database.backup')
            error = "Database backup error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    @http.route('/web/database/restore', type='http', auth="none", methods=['POST'], csrf=False)
    def restore(self, master_pwd, backup_file, name, copy=False):
        try:
            data_file = None
            db.check_super(master_pwd)
            with tempfile.NamedTemporaryFile(delete=False) as data_file:
                backup_file.save(data_file)
            db.restore_db(name, data_file.name, str2bool(copy))
            return http.local_redirect('/web/database/manager')
        except Exception as e:
            error = "Database restore error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)
        finally:
            if data_file:
                os.unlink(data_file.name)

    @http.route('/web/database/change_password', type='http', auth="none", methods=['POST'], csrf=False)
    def change_password(self, master_pwd, master_pwd_new):
        try:
            dispatch_rpc('db', 'change_admin_password', [master_pwd, master_pwd_new])
            return http.local_redirect('/web/database/manager')
        except Exception as e:
            error = "Master password update error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)

    @http.route('/web/database/list', type='json', auth='none')
    def list(self):
        """
        Used by Mobile application for listing database
        :return: List of databases
        :rtype: list
        """
        return http.db_list()
    
class Session(http.Controller):

    @http.route('/web/session/get_session_info', type='json', auth="none")
    def get_session_info(self):
        request.session.check_security()
        request.uid = request.session.uid
        request.disable_db = False
        return request.env['ir.http'].session_info()

    @http.route('/web/session/authenticate', type='json', auth="none", cors='*') # cors added to enable connection from android APP
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/web/session/change_password', type='json', auth="user")
    def change_password(self, fields):
        old_password, new_password,confirm_password = operator.itemgetter('old_pwd', 'new_password','confirm_pwd')(
            {f['name']: f['value'] for f in fields})
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error':_('You cannot leave any password empty.'),'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),'title': _('Change Password')}

        msg = _("Error, password not changed !")
        try:
            if request.env['res.users'].change_password(old_password, new_password):
                return {'new_password':new_password}
        except UserError as e:
            msg = e.name
        except AccessDenied as e:
            msg = e.args[0]
            if msg == AccessDenied().args[0]:
                msg = _('The old password you provided is incorrect, your password was not changed.')
        return {'title': _('Change Password'), 'error': msg}

    @http.route('/web/session/get_lang_list', type='json', auth="none")
    def get_lang_list(self):
        try:
            return dispatch_rpc('db', 'list_lang', []) or []
        except Exception as e:
            return {"error": e, "title": _("Languages")}

    @http.route('/web/session/modules', type='json', auth="user")
    def modules(self):
        # return all installed modules. Web client is smart enough to not load a module twice
        return module_installed(environment=request.env(user=odoo.SUPERUSER_ID))

    @http.route('/web/session/save_session_action', type='json', auth="user")
    def save_session_action(self, the_action):
        """
        This method store an action object in the session object and returns an integer
        identifying that action. The method get_session_action() can be used to get
        back the action.

        :param the_action: The action to save in the session.
        :type the_action: anything
        :return: A key identifying the saved action.
        :rtype: integer
        """
        return request.session.save_action(the_action)

    @http.route('/web/session/get_session_action', type='json', auth="user")
    def get_session_action(self, key):
        """
        Gets back a previously saved action. This method can return None if the action
        was saved since too much time (this case should be handled in a smart way).

        :param key: The key given by save_session_action()
        :type key: integer
        :return: The saved action or None.
        :rtype: anything
        """
        return request.session.get_action(key)

    @http.route('/web/session/check', type='json', auth="user")
    def check(self):
        request.session.check_security()
        return None

    @http.route('/web/session/account', type='json', auth="user")
    def account(self):
        ICP = request.env['ir.config_parameter'].sudo()
        params = {
            'response_type': 'token',
            'client_id': ICP.get_param('database.uuid') or '',
            'state': json.dumps({'d': request.db, 'u': ICP.get_param('web.base.url')}),
            'scope': 'userinfo',
        }
        return 'https://accounts.odoo.com/oauth2/auth?' + werkzeug.url_encode(params)

    @http.route('/web/session/destroy', type='json', auth="user")
    def destroy(self):
        request.session.logout()

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect(redirect, 303)
    
    
    
class Binary(http.Controller):

    def placeholder(self, image='placeholder.png'):
        with tools.file_open(get_resource_path('web', 'static/src/img', image), 'rb') as fd:
            return fd.read()

    @http.route(['/web/content',
        '/web/content/<string:xmlid>',
        '/web/content/<string:xmlid>/<string:filename>',
        '/web/content/<int:id>',
        '/web/content/<int:id>/<string:filename>',
        '/web/content/<int:id>-<string:unique>',
        '/web/content/<int:id>-<string:unique>/<string:filename>',
        '/web/content/<int:id>-<string:unique>/<path:extra>/<string:filename>',
        '/web/content/<string:model>/<int:id>/<string:field>',
        '/web/content/<string:model>/<int:id>/<string:field>/<string:filename>'], type='http', auth="public")
    def content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       filename=None, filename_field='name', unique=None, mimetype=None,
                       download=None, data=None, token=None, access_token=None, **kw):

        status, headers, content = request.env['ir.http'].binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype, access_token=access_token)

        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        if token:
            response.set_cookie('fileToken', token)
        return response

    @http.route(['/web/partner_image',
        '/web/partner_image/<int:rec_id>',
        '/web/partner_image/<int:rec_id>/<string:field>',
        '/web/partner_image/<int:rec_id>/<string:field>/<string:model>/'], type='http', auth="public")
    def content_image_partner(self, rec_id, field='image_128', model='res.partner', **kwargs):
        # other kwargs are ignored on purpose
        return self._content_image(id=rec_id, model='res.partner', field=field,
            placeholder='user_placeholder.jpg')

    @http.route(['/web/image',
        '/web/image/<string:xmlid>',
        '/web/image/<string:xmlid>/<string:filename>',
        '/web/image/<string:xmlid>/<int:width>x<int:height>',
        '/web/image/<string:xmlid>/<int:width>x<int:height>/<string:filename>',
        '/web/image/<string:model>/<int:id>/<string:field>',
        '/web/image/<string:model>/<int:id>/<string:field>/<string:filename>',
        '/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>',
        '/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>/<string:filename>',
        '/web/image/<int:id>',
        '/web/image/<int:id>/<string:filename>',
        '/web/image/<int:id>/<int:width>x<int:height>',
        '/web/image/<int:id>/<int:width>x<int:height>/<string:filename>',
        '/web/image/<int:id>-<string:unique>',
        '/web/image/<int:id>-<string:unique>/<string:filename>',
        '/web/image/<int:id>-<string:unique>/<int:width>x<int:height>',
        '/web/image/<int:id>-<string:unique>/<int:width>x<int:height>/<string:filename>'], type='http', auth="public")
    def content_image(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                      filename_field='name', unique=None, filename=None, mimetype=None,
                      download=None, width=0, height=0, crop=False, access_token=None,
                      **kwargs):
        # other kwargs are ignored on purpose
        return self._content_image(xmlid=xmlid, model=model, id=id, field=field,
            filename_field=filename_field, unique=unique, filename=filename, mimetype=mimetype,
            download=download, width=width, height=height, crop=crop,
            quality=int(kwargs.get('quality', 0)), access_token=access_token)

    def _content_image(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       filename_field='name', unique=None, filename=None, mimetype=None,
                       download=None, width=0, height=0, crop=False, quality=0, access_token=None,
                       placeholder='placeholder.png', **kwargs):
        status, headers, image_base64 = request.env['ir.http'].binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype,
            default_mimetype='image/png', access_token=access_token)

        if status in [301, 304] or (status != 200 and download):
            return request.env['ir.http']._response_by_status(status, headers, image_base64)
        if not image_base64:
            # Since we set a placeholder for any missing image, the status must be 200. In case one
            # wants to configure a specific 404 page (e.g. though nginx), a 404 status will cause
            # troubles.
            status = 200
            image_base64 = base64.b64encode(self.placeholder(image=placeholder))
            if not (width or height):
                width, height = odoo.tools.image_guess_size_from_field_name(field)

        image_base64 = image_process(image_base64, size=(int(width), int(height)), crop=crop, quality=int(quality))

        content = base64.b64decode(image_base64)
        headers = http.set_safe_image_headers(headers, content)
        response = request.make_response(content, headers)
        response.status_code = status
        return response

    # backward compatibility
    @http.route(['/web/binary/image'], type='http', auth="public")
    def content_image_backward_compatibility(self, model, id, field, resize=None, **kw):
        width = None
        height = None
        if resize:
            width, height = resize.split(",")
        return self.content_image(model=model, id=id, field=field, width=width, height=height)


    

    

    @http.route([
        '/web/binary/company_logo',
        '/logo',
        '/logo.png',
    ], type='http', auth="none", cors="*")
    def company_logo(self, dbname=None, **kw):
        imgname = 'logo'
        imgext = '.png'
        placeholder = functools.partial(get_resource_path, 'web', 'static', 'src', 'img')
        uid = None
        if request.session.db:
            dbname = request.session.db
            uid = request.session.uid
        elif dbname is None:
            dbname = db_monodb()

        if not uid:
            uid = odoo.SUPERUSER_ID

        if not dbname:
            response = http.send_file(placeholder(imgname + imgext))
        else:
            try:
                # create an empty registry
                registry = odoo.modules.registry.Registry(dbname)
                with registry.cursor() as cr:
                    company = int(kw['company']) if kw and kw.get('company') else False
                    if company:
                        cr.execute("""SELECT logo_web, write_date
                                        FROM res_company
                                       WHERE id = %s
                                   """, (company,))
                    else:
                        cr.execute("""SELECT c.logo_web, c.write_date
                                        FROM res_users u
                                   LEFT JOIN res_company c
                                          ON c.id = u.company_id
                                       WHERE u.id = %s
                                   """, (uid,))
                    row = cr.fetchone()
                    if row and row[0]:
                        image_base64 = base64.b64decode(row[0])
                        image_data = io.BytesIO(image_base64)
                        mimetype = guess_mimetype(image_base64, default='image/png')
                        imgext = '.' + mimetype.split('/')[1]
                        if imgext == '.svg+xml':
                            imgext = '.svg'
                        response = http.send_file(image_data, filename=imgname + imgext, mimetype=mimetype, mtime=row[1])
                    else:
                        response = http.send_file(placeholder('nologo.png'))
            except Exception:
                response = http.send_file(placeholder(imgname + imgext))

        return response

    @http.route(['/web/sign/get_fonts','/web/sign/get_fonts/<string:fontname>'], type='json', auth='public')
    def get_fonts(self, fontname=None):
        """This route will return a list of base64 encoded fonts.

        Those fonts will be proposed to the user when creating a signature
        using mode 'auto'.

        :return: base64 encoded fonts
        :rtype: list
        """


        fonts = []
        if fontname:
            module_path = get_module_path('web')
            fonts_folder_path = os.path.join(module_path, 'static/src/fonts/sign/')
            module_resource_path = get_resource_path('web', 'static/src/fonts/sign/' + fontname)
            if fonts_folder_path and module_resource_path:
                fonts_folder_path = os.path.join(os.path.normpath(fonts_folder_path), '')
                module_resource_path = os.path.normpath(module_resource_path)
                if module_resource_path.startswith(fonts_folder_path):
                    with file_open(module_resource_path, 'rb') as font_file:
                        font = base64.b64encode(font_file.read())
                        fonts.append(font)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            fonts_directory = os.path.join(current_dir, '..', 'static', 'src', 'fonts', 'sign')
            font_filenames = sorted(os.listdir(fonts_directory))

            for filename in font_filenames:
                font_file = open(os.path.join(fonts_directory, filename), 'rb')
                font = base64.b64encode(font_file.read())
                fonts.append(font)
        return fonts
    
    
    
 
