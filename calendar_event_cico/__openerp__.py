# -*- coding: utf-8 -*-
{
    'name': "Calendar Event CheckIn/Out",

    'summary': """


        """,

    'description': """



    """,

    'author': 'Odoo CN, Jeffery <jeffery9@gmail.com>',
    'website': "http://www.odoouse.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['calendar', 'hr_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}
