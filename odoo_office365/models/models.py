# -*- coding: utf-8 -*-

import logging
import re

from odoo import fields, models, api, osv
from odoo.exceptions import ValidationError

from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
from odoo.exceptions import UserError, AccessError
import requests
import json
from datetime import datetime
import time
from datetime import timedelta

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/]{3,}=*)([\'"])', re.I)


class OfficeSettings(models.Model):
    """
    This class separates one time office 365 settings from Token generation settings
    """
    _name = "office.settings"
    _description = "Office365/Credentials"

    field_name = fields.Char('Office365')
    
    redirect_url = fields.Char('Redirect URL')
    client_id = fields.Char('Client Id')
    secret = fields.Char('Secret')
    login_url = fields.Char('Login URL', compute='_compute_url', readonly=True)

    @api.depends('redirect_url','client_id','secret')
    def _compute_url(self):

        settings = self.env['office.settings'].search([])
        settings = settings[0] if settings else settings
        if settings:
            self.login_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?' \
                             'client_id=%s&redirect_uri=%s&response_type=code&scope=openid+offline_access+' \
                             'Calendars.ReadWrite+Mail.ReadWrite+Mail.Send+User.ReadWrite+Tasks.ReadWrite+' \
                             'Contacts.ReadWrite+MailboxSettings.Read' % (
                self.client_id, self.redirect_url)

    def save_data(self):
        try:
            if not self.client_id or not self.redirect_url or not self.secret:
                 raise osv.except_osv(_("Wrong Credentials!"), (_("Please Check your Credentials and try again")))
            else:
                self.env.user.redirect_url = self.redirect_url
                self.env.user.client_id = self.client_id
                self.env.user.secret = self.secret
                self.env.user.code = None
                self.env.user.token = None
                self.env.user.refresh_token = None
                self.env.user.expires_in = None
                self.env.user.office365_email = None
                self.env.user.office365_id_address = None

                self.env.cr.commit()
                context = dict(self._context)
                # self.env['office.usersettings'].login_url
                context['message'] = 'Successfully Saved!'
                return self.message_wizard(context)

        except Exception as e:
            raise ValidationError(_(str(e)))

    def message_wizard(self, context):

        return {
            'name': ('Success'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context

        }

        # raise osv.except_osv(_("Success!"), (_("Successfully Saved!")))


class Office365UserSettings(models.Model):
    """
    This class facilitates the users other than admin to enter office 365 credential
    """
    _name = 'office.usersettings'
    _description = "Office/Usersttings"
    login_url = fields.Char('Login URL', compute='_compute_url', readonly=True)
    code = fields.Char('code')
    field_name = fields.Char('office')
    token = fields.Char('Office_Token')

    def _compute_url(self):
        settings = self.env['office.settings'].search([])
        settings = settings[0] if settings else settings
        if settings:
            self.login_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?' \
                             'client_id=%s&redirect_uri=%s&response_type=code&scope=openid+' \
                             'offline_access+Calendars.ReadWrite+Mail.ReadWrite+Mail.Send+User.ReadWrite+' \
                             'Tasks.ReadWrite+Contacts.ReadWrite+MailboxSettings.Read' % (
                settings.client_id, settings.redirect_url)

    def generate_token(self, code):

        try:
            settings = self.env['office.settings'].search([])
            settings = settings[0] if settings else settings

            if not settings.client_id or not settings.redirect_url or not settings.secret:
                raise osv.except_osv(_("Error!"), (_("Please ask admin to add Office365 settings!")))

            header = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(
                'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                data='grant_type=authorization_code&code=' + code + '&redirect_uri=' + settings.redirect_url + '&client_id=' + settings.client_id + '&client_secret=' + settings.secret
                , headers=header).content

            if 'error' in json.loads(response.decode('utf-8')) and json.loads(response.decode('utf-8'))['error']:
                raise UserError('Invalid Credentials . Please! Check your credential and  regenerate the code and try again!')

            else :
                data = {}
                response = json.loads((str(response)[2:])[:-1])
                data['token'] =response['access_token']
                data['refresh_token'] =response['refresh_token']
                data['expires_in'] =response['expires_in']

                categories = requests.get('https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
                                          headers={
                                              'Host': 'outlook.office.com',
                                              'Authorization': 'Bearer {0}'.format(data['token']),
                                              'Accept': 'application/json',
                                              'X-Target-URL': 'http://outlook.office.com',
                                              'connection': 'keep-Alive'
                                          }).content
                category = json.loads(categories.decode('utf-8'))

                odoo_categ = self.env['calendar.event.type']

                if 'value' in category:

                    for categ in category['value']:
                        if  self.env['calendar.event.type'].search(
                                    ['|', ('categ_id', '=', categ['id']), ('name', '=', categ['displayName'])]):
                            # office_categ.write({'categ_id': categ['id'],
                            #                     'color': categ['color'],
                            #                     'name': categ['displayName'],
                            #                     })
                            odoo_categ.write({'categ_id': categ['id'],
                                              'color': categ['color'],
                                              'name': categ['displayName'],
                                              })
                        else:
                            # office_categ.create({'categ_id': categ['id'],
                            #                      'color': categ['color'],
                            #                      'name': categ['displayName'],
                            #                      })
                            odoo_categ.create({'categ_id': categ['id'],
                                               'color': categ['color'],
                                               'name': categ['displayName'],
                                               })

                    response = json.loads((requests.get(
                        'https://graph.microsoft.com/v1.0/me',
                        headers={
                            'Host': 'outlook.office.com',
                            'Authorization': 'Bearer {0}'.format(data['token']),
                            'Accept': 'application/json',
                            'X-Target-URL': 'http://outlook.office.com',
                            'connection': 'keep-Alive'
                        }).content.decode('utf-8')))
                    if response:
                        data['userPrincipalName'] = response['userPrincipalName']
                        data['office365_id_address'] = 'outlook_' + response['id'].upper() + '@outlook.com'

                if 'token' in data:
                    self.get_calendars(data)
                return data

        except Exception as e:
            _logger.error(e)
            data['error']=e
            return data

    def get_calendars(self, data):
        try:
            calendars_response = requests.get('https://graph.microsoft.com/v1.0/me/calendars',
                                      headers={
                                          'Host': 'outlook.office.com',
                                          'Authorization': 'Bearer {0}'.format(data['token']),
                                          'Accept': 'application/json',
                                          'X-Target-URL': 'http://outlook.office.com',
                                          'connection': 'keep-Alive'
                                      }).content
            calendars = json.loads(calendars_response.decode('utf-8'))
            office_connector = self.env['office.sync'].search([])[0]
            if 'value' in calendars:
                odoo_calendar = self.env['office.calendars'].search([])
                odoo_calendar.unlink()
                odoo_calendar = self.env['office.calendars']
                for calendar in calendars['value']:
                    if odoo_calendar.search([('calendar_id','=',calendar['id'])]):
                        odoo_calendar.write({'calendar_id': calendar['id'],
                            'name': calendar['name'],
                            'res_user': self.env.user.id,
                            # 'connector_id':office_connector.id

                        })
                    else:
                        odoo_calendar.create({'calendar_id': calendar['id'],
                                             'name': calendar['name'],
                                             'res_user': self.env.user.id,
                                            # 'connector_id': office_connector.id

                                             })
        except Exception as e:
            _logger.error("API ERROR: {}".format(e))
            pass


class CustomUser(models.Model):
    """
    Add custom fields for office365 users
    """
    _inherit = 'res.users'

    login_url = fields.Char('Login URL', compute='_compute_url', readonly=True)
    code = fields.Char('code')
    token = fields.Char('Token', readonly=True)
    refresh_token = fields.Char('Refresh Token', readonly=True)
    expires_in = fields.Char('Expires IN', readonly=True)
    redirect_url = fields.Char('Redirect URL')
    client_id = fields.Char('Client Id')
    secret = fields.Char('Secret')
    office365_email = fields.Char('Office365 Email Address', readonly=True)
    office365_id_address = fields.Char('Office365 Id Address', readonly=True)
    send_mail_flag = fields.Boolean(string='Send messages using office365 Mail', default=True)
    is_task_sync_on = fields.Boolean('is sync in progress', default=False)
    last_mail_import = fields.Datetime(string="Last Import", required=False, readonly=True)
    last_calender_import = fields.Datetime(string="Last Import", required=False, readonly=True)
    last_task_import = fields.Datetime(string="Last Import", required=False, readonly=True)
    last_contact_import = fields.Datetime(string="Last Import", required=False, readonly=True)
    event_del_flag = fields.Boolean('Delete events from Office365 calendar when delete in Odoo.',groups="base.group_user")
    event_create_flag = fields.Boolean('Create events in Office365 calendar when create in Odoo.')
    office365_event_del_flag = fields.Boolean('Delete event from Odoo, if the event is deleted from Office 365.', groups="base.group_user")

    # calendar_id = fields.One2many(comodel_name="office.calendars", inverse_name="res_user", string="Office365 Calendars", required=False, )
    calendar_id = fields.Many2one(comodel_name="office.calendars", string="Office365 Calendars", required=False, )

    def get_code(self):

        context = dict(self._context)
        settings = self.env['office.settings'].search([])
        if settings.redirect_url and settings.client_id and settings.login_url:
            if self.id == self.env.user.id:

                # return self.message_wizard(context)
                return {
                    'name': 'login',
                    'view_id': False,
                    "type": "ir.actions.act_url",
                    'target': 'self',
                    'url': settings.login_url
                }
        else:
            raise ValidationError('Office365 Credentials are missing. Please! ask admin to add Office365 Client id, '
                                      'client secret and redirect Url ')


class CustomMeeting(models.Model):
    """
    adding office365 event ID to ODOO meeting to remove duplication and facilitate updation
    """
    _inherit = 'calendar.event'
    office_id = fields.Char('Office365 Id')
    category_name = fields.Char('Categories', )
    is_update = fields.Boolean('Is Updated')
    modified_date = fields.Datetime('Modified Date')
    calendar_id = fields.Many2one(comodel_name="office.calendars", string="Office Calendar Id", required=False, )

    # @api.multi
    def write(self, values):
        # Add code here
        if 'is_update' in values:
            return super(CustomMeeting, self).write(values)
        else:
            if 'office_id' not in values:
                values['is_update'] = True
                values['modified_date'] = datetime.now()
            return super(CustomMeeting, self).write(values)

    @api.onchange('categ_ids')
    def chnage_category(self):
        if self.categ_ids:
            self.category_name = self.categ_ids[0].name

    # multi
    def unlink(self):
        events = self
        for self in events:
            if self.office_id and self.env.user.event_del_flag:
                if self.env.user.expires_in:
                    expires_in = datetime.fromtimestamp(int(self.env.user.expires_in) / 1e3)
                    expires_in = expires_in + timedelta(seconds=3600)
                    nowDateTime = datetime.now()
                    if nowDateTime > expires_in:
                        self.env['res.users'].generate_refresh_token()
                header = {
                    'Authorization': 'Bearer {0}'.format(self.env.user.token),
                    'Content-Type': 'application/json'
                }

                response = requests.get(
                    'https://graph.microsoft.com/v1.0/me/calendars',
                    headers={
                        'Host': 'outlook.office.com',
                        'Authorization': 'Bearer {0}'.format(self.env.user.token),
                        'Accept': 'application/json',
                        'X-Target-URL': 'http://outlook.office.com',
                        'connection': 'keep-Alive'
                    }).content
                if 'value' not in json.loads((response.decode('utf-8'))).keys():
                    raise osv.except_osv(("Access Token Expired!"), (" Please Regenerate Access Token !"))
                calendars = json.loads((response.decode('utf-8')))['value']
                calendar_id = calendars[0]['id']
                response = requests.delete(
                    'https://graph.microsoft.com/v1.0/me/calendars/' + calendar_id + '/events/' + self.office_id,
                    headers=header)
                if response.status_code == 204:
                    _logger.info('successfull deleted event ' + self.name+"from Office365 Calendar")
                    # res = super(CustomMeeting, self).unlink(self)
                res = super(CustomMeeting, self).unlink(self)
            else:
                res = super(CustomMeeting, self).unlink(self)

        return res


class CustomMessageInbox(models.Model):
    """
    Email will store in mail.message class so that's why we need office_id
    """
    _inherit = 'mail.message'
    office_id = fields.Char('Office Id')


class CustomMessage(models.Model):

    # Email will be sent to the recipient of the message.
    _inherit = 'mail.mail'
    office_id = fields.Char('Office Id')

    @api.model
    def create(self, values):
        """
        overriding create message to send email on message creation
        :param values:
        :return:
        """
        ################## New Code ##################
        ################## New Code ##################
        o365_id = None
        conv_id = None
        context = self._context

        current_uid = context.get('uid')

        user = self.env['res.users'].browse(current_uid)
        if user.send_mail_flag:
            if user.token:
                if user.expires_in:
                    expires_in = datetime.fromtimestamp(int(user.expires_in) / 1e3)
                    expires_in = expires_in + timedelta(seconds=3600)
                    nowDateTime = datetime.now()
                    if nowDateTime > expires_in:
                        self.generate_refresh_token()
                if 'mail_message_id' in values:
                    email_obj = self.env['mail.message'].search([('id', '=', values['mail_message_id'])])
                    partner_id = values['recipient_ids'][0][1]
                    partner_obj = self.env['res.partner'].search([('id', '=', partner_id)])

                    new_data = {
                                "subject": values['subject'] if values['subject'] else email_obj.body,
                                # "importance": "high",
                                "body": {
                                    "contentType": "HTML",
                                    "content": email_obj.body
                                },
                                "toRecipients": [
                                    {
                                        "emailAddress": {
                                            "address": partner_obj.email
                                        }
                                    }
                                ]
                            }

                    response = requests.post(
                        'https://graph.microsoft.com/v1.0/me/messages', data=json.dumps(new_data),
                                            headers={
                                                'Host': 'outlook.office.com',
                                                'Authorization': 'Bearer {0}'.format(user.token),
                                                'Accept': 'application/json',
                                                'Content-Type': 'application/json',
                                                'X-Target-URL': 'http://outlook.office.com',
                                                'connection': 'keep-Alive'
                                            })
                    if 'conversationId' in json.loads((response.content.decode('utf-8'))).keys():
                        conv_id = json.loads((response.content.decode('utf-8')))['conversationId']

                    if 'id' in json.loads((response.content.decode('utf-8'))).keys():

                        o365_id = json.loads((response.content.decode('utf-8')))['id']
                        if email_obj.attachment_ids:
                            for attachment in self.getAttachments(email_obj.attachment_ids):
                                attachment_response = requests.post(
                                    'https://graph.microsoft.com/beta/me/messages/' + o365_id + '/attachments',
                                    data=json.dumps(attachment),
                                    headers={
                                        'Host': 'outlook.office.com',
                                        'Authorization': 'Bearer {0}'.format(user.token),
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json',
                                        'X-Target-URL': 'http://outlook.office.com',
                                        'connection': 'keep-Alive'
                                    })
                        send_response = requests.post(
                            'https://graph.microsoft.com/v1.0/me/messages/' + o365_id + '/send',
                            headers={
                                'Host': 'outlook.office.com',
                                'Authorization': 'Bearer {0}'.format(user.token),
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'X-Target-URL': 'http://outlook.office.com',
                                'connection': 'keep-Alive'
                            })

                        message = super(CustomMessage, self).create(values)
                        message.email_from = None

                        if conv_id:
                            message.office_id = conv_id

                        return message
                    else:
                        pass
                        # print('Check your credentials! Mail does not send due to invlide office365 credentials ')

                else:

                    return super(CustomMessage, self).create(values)

            else:
                # print('Office354 Token is missing.. Please add your account token and try again!')
                return super(CustomMessage, self).create(values)

        else:
            return super(CustomMessage, self).create(values)

    def getAttachments(self, attachment_ids):
        attachment_list = []
        if attachment_ids:
            # attachments = self.env['ir.attachment'].browse([id[0] for id in attachment_ids])
            attachments = self.env['ir.attachment'].search([('id', 'in', [i.id for i in attachment_ids])])
            for attachment in attachments:
                attachment_list.append({
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": attachment.name,
                    "contentBytes": attachment.datas.decode("utf-8")
                })
        return attachment_list

    def generate_refresh_token(self):
        context = self._context

        current_uid = context.get('uid')

        user = self.env['res.users'].browse(current_uid)
        if user.refresh_token:
            settings = self.env['office.settings'].search([])
            settings = settings[0] if settings else settings

            if not settings.client_id or not settings.redirect_url or not settings.secret:
                raise osv.except_osv(_("Error!"), (_("Please ask admin to add Office365 settings!")))
            header = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }


            response = requests.post(
                'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                data='grant_type=refresh_token&refresh_token=' + user.refresh_token + '&redirect_uri=' + settings.redirect_url + '&client_id=' + settings.client_id + '&client_secret=' + settings.secret
                , headers=header)
                #.content

            # response = json.loads((str(response)[2:])[:-1])
            res_data = json.loads(response.content.decode("utf-8"))
            if 'access_token' not in res_data:
                res_data["error_description"] = res_data["error_description"].replace("\\r\\n", " ")
                raise osv.except_osv(_("Error!"), (_(res_data["error"] + " " + res_data["error_description"])))
            else:
                user.token = res_data['access_token']
                user.refresh_token = res_data['refresh_token']
                user.expires_in = int(round(time.time() * 1000))
                self.env.cr.commit()


class CustomActivity(models.Model):
    _inherit = 'mail.activity'

    office_id = fields.Char('Office365 Id')
    is_update = fields.Boolean('Is Updated')
    modified_date = fields.Datetime('Modified Date')

    # @api.multi
    def write(self, values):
        # Add code here
        if 'is_update' in values:
            return super(CustomActivity, self).write(values)
        else:
            if 'office_id' not in values:
                values['is_update'] = True
                values['modified_date'] = datetime.now()
            return super(CustomActivity, self).write(values)

    @api.model
    def create(self, values):
        if self.env.user.expires_in:
            expires_in = datetime.fromtimestamp(int(self.env.user.expires_in) / 1e3)
            expires_in = expires_in + timedelta(seconds=3600)
            nowDateTime = datetime.now()
            if nowDateTime > expires_in:
                self.generate_refresh_token()

        o365_id = None
        if self.env.user.office365_email and not self.env.user.is_task_sync_on and values[
            'res_id'] == self.env.user.partner_id.id:
            data = {
                'subject': values['summary'] if values['summary'] else values['note'],
                "body": {
                    "contentType": "html",
                    "content": values['note']
                },
                "dueDateTime": {
                    "dateTime": values['date_deadline'] + 'T00:00:00Z',
                    "timeZone": "UTC"
                },
            }
            response = requests.post(
                'https://graph.microsoft.com/beta/me/outlook/tasks', data=json.dumps(data),
                headers={
                    'Host': 'outlook.office.com',
                    'Authorization': 'Bearer {0}'.format(self.env.user.token),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-Target-URL': 'http://outlook.office.com',
                    'connection': 'keep-Alive'
                }).content
            if 'id' in json.loads((response.decode('utf-8'))).keys():
                o365_id = json.loads((response.decode('utf-8')))['id']

        """
        original code!
        """

        activity = super(CustomActivity, self).create(values)
        self.env[activity.res_model].browse(activity.res_id).message_subscribe(
            partner_ids=[activity.user_id.partner_id.id])
        if activity.date_deadline <= fields.Date.today():
            self.env['bus.bus'].sendone(
                (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                {'type': 'activity_updated', 'activity_created': True})
        if o365_id:
            activity.office_id = o365_id
        return activity

    def generate_refresh_token(self):

        if self.env.user.refresh_token:
            settings = self.env['office.settings'].search([])
            settings = settings[0] if settings else settings

            if not settings.client_id or not settings.redirect_url or not settings.secret:
                raise osv.except_osv(_("Error!"), (_("Please ask admin to add Office365 settings!")))

            header = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(
                'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                data='grant_type=refresh_token&refresh_token=' + self.env.user.refresh_token + '&redirect_uri=' + settings.redirect_url + '&client_id=' + settings.client_id + '&client_secret=' + settings.secret
                , headers=header).content

            # response = json.loads((str(response)[2:])[:-1])
            res_data = json.load(response)
            if 'access_token' not in res_data:
                res_data["error_description"] = res_data["error_description"].replace("\\r\\n", " ")
                raise osv.except_osv(("Error!"), (res_data["error"] + " " + res_data["error_description"]))
            else:
                self.env.user.token = res_data['access_token']
                self.env.user.refresh_token = res_data['refresh_token']
                self.env.user.expires_in = int(round(time.time() * 1000))

    # @api.multi
    def unlink(self):
        for activity in self:
            if activity.office_id:
                response = requests.delete(
                    'https://graph.microsoft.com/beta/me/outlook/tasks/' + activity.office_id,
                    headers={
                        'Host': 'outlook.office.com',
                        'Authorization': 'Bearer {0}'.format(self.env.user.token),
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-Target-URL': 'http://outlook.office.com',
                        'connection': 'keep-Alive'
                    })
                if response.status_code != 204 and response.status_code != 404:
                    raise osv.except_osv(_("Office365 SYNC ERROR"), (_("Error: " + str(response.status_code))))
            if activity.date_deadline <= fields.Date.today():
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                    {'type': 'activity_updated', 'activity_deleted': True})
        return super(CustomActivity, self).unlink()


class CustomContacts(models.Model):

    _inherit = 'res.partner'

    office_contact_id = fields.Char('Office365 Id')
    is_update = fields.Boolean(string="Is update",default=True)
    # is_create = fields.Boolean(string="Is create", default=True  )
    modified_date = fields.Datetime('Modified Date')
    location = fields.Char(string='Location')

    # @api.multi
    def write(self, values):
        # Add code here
        if 'is_update' in values:
            return super(CustomContacts, self).write(values)
        else:
            if 'office_contact_id' not in values:
                values['is_update'] = True
                values['modified_date'] = datetime.now()
            return super(CustomContacts, self).write(values)

    # @api.model
    # def create(self, values):
    #     # Add code here
    #     if 'is_create' in values:
    #         return super(CustomContacts, self).create(values)
    #     else:
    #         if 'office_contact_id' not in values:
    #             values['is_create'] = True
    #         return super(CustomContacts, self).create(values)


class CalendarEventCateg(models.Model):
    _inherit = 'calendar.event.type'
    color = fields.Char(string="Color", required=False, )
    categ_id = fields.Char(string="o_category id", required=False, )


class OfficeCalendars(models.Model):
    _name = "office.calendars"
    _description = "office365/Calendars"
    calendar_id = fields.Char(string="Office Calendar ID", required=False, )
    name = fields.Char(string="Calendar Name", required=False, )
    res_user = fields.Many2one(comodel_name="res.users", string="User", required=False, )
    # connector_id = fields.Many2one(comodel_name="office.sync", string="reference connector", required=False, )

