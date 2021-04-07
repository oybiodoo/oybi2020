# -*- coding: utf-8 -*-
{
    'name': "Odoo Office 365 Connector",

    'summary': """
                Odoo Office365 Connector provides the opportunity to sync calendar, contacts, tasks and mails between ODOO and Office365.
            """,

    'description': """
    Odoo is a fully integrated suite of business modules that encompass the traditional ERP functionality. Odoo office 365 Connector 		provides the opportunity to sync calendar, contacts,task and mail between ODOO and office 365.
    """,
    'author': "Techloyce",
    'website': "http://www.techloyce.com",
    'category': 'sale',
    'price': 499,
    'currency': 'EUR',
    'version': '13.3.3',
    'license': 'OPL-1',
    'depends': ['base', 'calendar', 'crm', 'hr'],
    'images': [
        'static/description/banner.gif',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/scheduler.xml',
        'wizard/message_wizard.xml',
        'views/template.xml',
        'views/office365_sync.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'live_test_url':'https://www.youtube.com/watch?v=gvuUiAsC-TM',
}
