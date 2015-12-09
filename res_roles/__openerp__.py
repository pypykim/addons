# -*- coding: utf-8 -*-
{
    'name': "User Role",

    'summary': """
        本模块定义了用户角色
        """,

    'description': """
       角色是比标准模块里面的用户组更高层次，更抽象的概念，角色可以具备多个用户组的权限。

    """,

    'author': "jeffery chen fan",
    'website': "http://www.odoouse.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [],

    # always loaded
    'data': [
        'templates.xml',
    ],
}
