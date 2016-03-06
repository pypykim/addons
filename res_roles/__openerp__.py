# -*- coding: utf-8 -*-
{
    'name': "用户角色",

    'summary': """
        本模块定义了用户角色
        """,

    'description': """
       角色是比标准模块里面的用户组更高层次，更抽象的概念，角色可以具备多个用户组的权限。

    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [],

    # always loaded
    'data': [
        'data.xml',
        'templates.xml',
        'security/roles.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
