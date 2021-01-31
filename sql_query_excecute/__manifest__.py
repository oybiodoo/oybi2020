# -*- coding: utf-8 -*-
{
    'name': "Sql Query Control",

    'summary': """
        Make data queries directly in odoo without having to enter postgres.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "JUVENTUD PRODUCTIVA VENEZOLANA",
    'website': "https://juventudproductivabicentenaria.blogspot.com/",
    'category': 'Extra tools',
    'version': '0.1',
    'license': 'AGPL-3',
    'depends': ['base_setup','mail'],
    'data': [
        'security/query_security.xml',
        'security/ir.model.access.csv',
        'views/view_insert_sql.xml',
    ],

    'demo': [
    ],
    'images': ['static/images/baner_screenshot.gif'],
    'application': True,
    'installable': True,
    'currency': 'EUR',
    'price': 30.00,
}
