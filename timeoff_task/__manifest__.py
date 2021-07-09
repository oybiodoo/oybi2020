# -*- coding: utf-8 -*-
{
    'name': "Time Off Task",

    'summary': """
        This module is developed to handle the functionality of adding
        a computed field over the Time Off view.""",

    'description': """
        This module is developed to handle the functionality of adding
        a computed field over the Time Off view.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '14.0.0.1',

    'depends': ['base', 'hr'],

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
