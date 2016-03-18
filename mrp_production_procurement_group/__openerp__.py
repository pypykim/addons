# -*- coding: utf-8 -*-
{
    'name': "Production procurement group",

    'summary': """
        """,

    'description': """
        add procurement group to MO, assign the MO name to procurement group if 
        it been created manually, otherwise use move_prod_id of the parent procurment order. 
    """,

    'author': 'Odoo CN, Jeffery <jeffery9@gmail.com>',
    'website': "http://www.odoouse.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}