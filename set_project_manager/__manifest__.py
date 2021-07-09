# -*- coding: utf-8 -*-
{
    'name': "Set Project Manager",

    'summary': """
        This module is developed to handle the customized requirements
        related to setting the project manager on sale order automatically.""",

    'description': """
        This module is developed to handle the customized requirements
        related to setting the project manager on sale order automatically.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '14.0.0.1',

    'depends': ['base', 'project'],

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
