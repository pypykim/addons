# -*- coding: utf-8 -*-

import time
import openerp.addons.decimal_precision as dp
from collections import OrderedDict
from openerp.osv import fields, osv, orm
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools import float_compare, float_is_zero
from openerp.tools.translate import _
from openerp import tools, SUPERUSER_ID
from openerp.addons.product import _common

class mrp_production(osv.osv):
    _inherit = 'mrp.production'

    _columns = {
        'procurement_group_id': fields.many2one('procurement.group', 'Procurement group', copy=False),
    }

    def create(self, cr, uid, vals, context=None):
        pg_var = {}
        if vals.has_key('name') and  vals['name']:
            pg_var['name'] = vals['name']

        elif vals.has_key('origin') and vals['origin']:
            pg_var['name'] = vals['origin']

        elif vals.has_key('move_prod_id') and vals['move_prod_id']:
            pg_var['name'] = vals['move_prod_id']

        else:
            pg_var['name'] = self.pool.get('ir.sequence').get(cr, uid, 'procurement.group')

        group_id = self.pool.get("procurement.group").create(cr, uid, pg_var, context=context)
        vals['procurement_group_id'] = group_id

        if context is None:
            context = {}
        result = super(mrp_production, self).create(cr, uid, vals, context=context)

        return result

    def _make_consume_line_from_data(self, cr, uid, production, product, uom_id, qty, uos_id, uos_qty, context=None):
        stock_move = self.pool.get('stock.move')
        loc_obj = self.pool.get('stock.location')
        # Internal shipment is created for Stockable and Consumer Products
        if product.type not in ('product', 'consu'):
            return False
        # Take routing location as a Source Location.
        source_location_id = production.location_src_id.id
        prod_location_id = source_location_id
        prev_move = False
        if production.bom_id.routing_id and production.bom_id.routing_id.location_id and production.bom_id.routing_id.location_id.id != source_location_id:
            source_location_id = production.bom_id.routing_id.location_id.id
            prev_move = True

        destination_location_id = production.product_id.property_stock_production.id
        move_id = stock_move.create(cr, uid, {
            'name': production.name,
            'date': production.date_planned,
            'date_expected': production.date_planned,
            'product_id': product.id,
            'product_uom_qty': qty,
            'product_uom': uom_id,
            'product_uos_qty': uos_id and uos_qty or False,
            'product_uos': uos_id or False,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'company_id': production.company_id.id,
            'procure_method': prev_move and 'make_to_stock' or self._get_raw_material_procure_method(cr, uid, product, location_id=source_location_id,
                                                                                                     location_dest_id=destination_location_id, context=context),  # Make_to_stock avoids creating procurement
            'raw_material_production_id': production.id,
            # this saves us a browse in create()
            'price_unit': product.standard_price,
            'origin': production.name,
            'warehouse_id': loc_obj.get_warehouse(cr, uid, production.location_src_id, context=context),
            'group_id': production.move_prod_id.group_id.id or production.procurement_group_id.id,
        }, context=context)

        if prev_move:
            prev_move = self._create_previous_move(cr, uid, move_id, product, prod_location_id, source_location_id, context=context)
            stock_move.action_confirm(cr, uid, [prev_move], context=context)
        return move_id
