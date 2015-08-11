# -*- coding: utf-8 -*-
{
    'name': "城市扩张",

    'summary': """
        本模块定义了城市与省份之前的关联关系

        """,

    'description': """
        本模块定义了城市与省份之前的关联关系
        1，城市限定于 省份
        2，一个维护城市的视图
        3，选择 城市时，自动切换所属的省份



    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],

    # always loaded
    'data': [
        'data.xml',
        'templates.xml',
        'security/roles.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
