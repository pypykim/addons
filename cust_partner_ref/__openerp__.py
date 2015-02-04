# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    'name': 'custom partner References',
    'version': '1.0',
    'category': 'Tools',
    'author': 'odoo-han Team',
    'contributors':"Jason Wu <jaronemo@msn.com>",
    'website':'',
    'summary': 'supplier/Customer Add References Code',
    'description': """
     customer reference code when partner check is customer
     supplier reference code when partner check is supplier
    """,
    'depends': ['base'],
    'data': [
        'views/res_partner_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}