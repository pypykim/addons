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
from openerp import models, fields, api, exceptions, _

class resbank(models.Model):
	_inherit ='res.bank'
	
	def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        	if not args:
            		args = []
		args = args[:]
		ids = []
	        if name:
	       	    ids = self.search(cr, user, [('bic', 'ilike', name)]+ args, limit=limit, context=context)
		    if not ids:
			ids = self.search(cr, user, [('name', 'ilike', name)]+ args, limit=limit, context=context)
        	else:
	            ids = self.search(cr, user, args, limit=limit, context=context)
		
		result = self.name_get(cr, user, ids, context=context)
		
		return result

class accountvoucherbills(models.Model):

	_inherit = 'account.voucher'

	check_name = fields.Char(string='Check Number', store=True, ondelete="cascade")
	bank_name = fields.Many2one('res.bank', string='Bank Name')
	
		
	@api.onchange('bank_name')
	def _onchange_reference(self):
		
		if self.bank_name and self.check_name:
			self.reference = '[' + self.check_name + ']' + ',' + self.bank_name.bic + ' - ' + self.bank_name.name
		
	@api.onchange('check_name')
	def _onchange_reference1(self):
		if self.check_name and self.bank_name:
			self.reference = '[' + self.check_name + ']' + ',' + self.bank_name.bic + ' - ' + self.bank_name.name
