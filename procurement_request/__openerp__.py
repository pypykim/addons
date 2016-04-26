# -*- coding: utf-8 -*-
{
    'name': "procurement_request",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "jeffery <jeffery9@gmail.com>",
    'website': "http://www.odoouse.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_stock', 'procurement'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'sequence.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}