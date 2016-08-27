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

class County(osv.Model):
    _description = "County"
    _name = 'res.country.county'
    _columns = {
        'city_id': fields.many2one('res.country.city', 'City',
                                    required=True),
        'name': fields.char('County Name', required=True,
                            help='County name of a country.'),

    }
    _order = 'name'

class res_partner(osv.Model):
    _inherit = "res.partner"

    _columns = {
        'county': fields.many2one("res.country.county", 'County', ondelete='restrict'),
        'city': fields.many2one("res.country.city", 'City', ondelete='restrict'),
        'identification': fields.selection([
            ('identity_card', 'Identity card'),
            ('passport', 'Passport'),
            ('driving_license', 'Driving license'),
            ('certificate_officer', 'Certificate officer'),
            ('other', u'Other'),
        ], string='Identification type'),
        'identification_code': fields.char('Identification code'),
        'organization_code': fields.char('Organization code'),
        'tax_registration': fields.char('Tax registration'),
        'qq': fields.char('QQ'),
        'wechat': fields.char('Wechat'),
    }

    def onchange_city(self, cr, uid, ids, city, context=None):
        if city:
            city_obj = self.pool.get('res.country.city').browse(cr, uid, city, context=context)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}

    def onchange_county(self, cr, uid, ids, county, context=None):
        if county:
            county_obj = self.pool.get('res.country.county').browse(cr, uid, county, context=context)
            return {'value': {'city_id': county_obj.city_id.id}}
        return {}

class crm_lead(osv.Model):
    _inherit = "crm.lead"

    _columns = {
        'county': fields.many2one("res.country.county", 'County'),
        'city': fields.many2one("res.country.city", 'City'),
        'qq': fields.char('QQ'),
        'website': fields.char('Website'),
    }

    def onchange_city(self, cr, uid, ids, city, context=None):
        if city:
            city_obj = self.pool.get('res.country.city').browse(cr, uid, city, context=context)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}

    def onchange_county(self, cr, uid, ids, county, context=None):
        if county:
            county_obj = self.pool.get('res.country.county').browse(cr, uid, county, context=context)
            return {'value': {'city_id': county_obj.city_id.id}}
        return {}
