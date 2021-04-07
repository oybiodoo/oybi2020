# -*- coding: utf-8 -*-
from datetime import datetime
import werkzeug
import werkzeug.utils
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
import time


class Office365Code(http.Controller):
    @http.route("/odoo", auth="public", type='http')
    def fetch_code(self, **kwargs):
        odoo_user = request.env['res.users'].sudo().search([('id', '=', request.env.user.id)])
        if "error" in kwargs:
            ValidationError(kwargs['error'])
        user_setting = request.env['office.usersettings'].sudo().search([], limit=1)
        if 'code' in kwargs:
            code = kwargs.get('code')
            if not user_setting:
                token = user_setting.generate_token(code)
                if not 'error' in token and 'token' in token:
                    odoo_user.token = token['token']
                    odoo_user.refresh_token = token['refresh_token']
                    # self.token = response['refresh_token']
                    odoo_user.expires_in = int(round(time.time() * 1000))
                    odoo_user.code = code
                    # odoo_user.code = ""
                    odoo_user.office365_email = token['userPrincipalName']
                    odoo_user.office365_id_address = token['office365_id_address']

                    request.env.cr.commit()

                    return request.render("odoo_office365.token_redirect_success_page")
                else:
                    return request.render("odoo_office365.token_redirect_fail_page")
            else:
                token = user_setting.generate_token(code)
                if token:
                    odoo_user.token = token['token']
                    odoo_user.refresh_token = token['refresh_token']
                    # self.token = response['refresh_token']
                    odoo_user.expires_in = int(round(time.time() * 1000))
                    odoo_user.code = code
                    # odoo_user.code = ""
                    odoo_user.office365_email = token['userPrincipalName']
                    odoo_user.office365_id_address = token['office365_id_address']

                    request.env.cr.commit()
                    return request.render("odoo_office365.token_redirect_success_page")
                else:
                    return request.render("odoo_office365.token_redirect_fail_page")

                # return werkzeug.utils.redirect("odoo_office365.token_redirect_success_page")
        else:
            return request.render("odoo_office365.token_redirect_fail_page")