# -*- coding: utf-8 -*-
{
    'name': "城市扩展",

    'summary': """
        本模块定义了县/市与省份之前的关联关系

        """,

    'description': """
        本模块定义了城市与省份之前的关联关系
        1，县/市限定于省份
        2，一个维护县/市的视图
        3，选择 县/市时，自动切换所属的省份

    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm','l10n_cn'],

    # always loaded
    'data': [
        'view.xml',
        'res.country.city.csv',
        'res.country.county.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
