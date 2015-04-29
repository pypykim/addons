# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Fix-up for Multiple Analytic Plans',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
This module allows to use several analytic plans according to the general journal.
==================================================================================

this is fix-up for the view definition.
    """,
    'author': 'Odoo CN Team, Jeffery Chen Fan <jeffery9@gmail.com>',
    'depends': ['account_analytic_analysis', 'account_analytic_default', 'account_analytic_plans'],
    'data': ['account_analytic_plans_view.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
