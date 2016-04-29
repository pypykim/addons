# -*- coding: utf-8 -*-
{
    'name': "Customize for Leave Management",

    'summary': """
        Customize for Leave Management""",

    'description': """
        Add default working time to company
        Employee can request leave in hours
        Add new group as department manager to do the first validation for leave request
    """,

    'author': "jeffery <jeffery9@gmail.com>",
    'website': "http://www.odoouse.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'hr_holidays_workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}