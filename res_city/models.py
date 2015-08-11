# -*- coding: utf-8 -*-
import openerp
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from lxml import etree
from lxml.builder import E
from openerp.tools.translate import _
from openerp.addons.base.res.res_users import name_boolean_group, name_selection_groups
from openerp import tools


class CountryCity(osv.Model):
    _description = "Country City"
    _name = 'res.country.city'
    _columns = {
        'state_id': fields.many2one('res.country.state', 'State',
                                    required=True),
        'name': fields.char('City Name', required=True,
                            help='City name of a country.'),

    }
    _order = 'name'

class res_partner(osv.Model):
    _inherit = "res.partner"

    _columns = {
        'city': fields.many2one("res.country.city", 'City', ondelete='restrict'),
        'identification': fields.selection([
            ('identity_card', u'身份证'),
            ('passport', u'护照'),
            ('driving_license', u'驾照'),
            ('certificate_officer', u'军官证'),
            ('other', u'其他'),
        ], string=u'证件类型'),
        'identification_code': fields.char(u'证件号码'),
        'organization_code': fields.char(u'组织机构代码'),
        'tax_registration': fields.char(u'税务登记号'),
    }

    def onchange_city(self, cr, uid, ids, city, context=None):
        if city:
            city_obj = self.pool.get('res.country.city').browse(cr, uid, city, context=context)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}

class crm_lead(osv.Model):
    _inherit = "crm.lead"

    def onchange_city(self, cr, uid, ids, city, context=None):
        if city:
            city_obj = self.pool.get('res.country.city').browse(cr, uid, city, context=context)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}