# -*- coding: utf-8 -*-
{
    'name': "CRM Opportunity",

    'summary': """
        This module is developed to handle the customized requirements
        of copying the lead title onto the quotation.""",

    'description': """
        This module is developed to handle the customized requirements
        of copying the lead title onto the quotation.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '14.0.0.1',

    'depends': ['base', 'crm', 'sale'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
