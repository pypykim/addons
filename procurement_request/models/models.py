# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

import logging

_logger = logging.getLogger(__name__)


class RequestOrder(models.Model):

    _name = 'request.order'
    _description = u'Request order'

    _rec_name = 'name'
    _order = 'name ASC'

    @api.multi
    def _employee_get(self, context=None):
        cr, uid = self.env.cr, self.env.uid
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        size=50,
        translate=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    employee_id = fields.Many2one(
        string='Employee',
        # default=lambda self: self._employee_get,
        comodel_name='hr.employee',
    )

    department_id = fields.Many2one(
        string='Department',
        comodel_name='hr.department',
        related ='employee_id.department_id',
        readonly="True"
    )

    partner_id = fields.Many2one('res.partner', string='Requstor', related ='employee_id.user_id.partner_id',  readonly="True")

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('request.order'))

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default=_default_warehouse_id)

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now)

    order_line = fields.One2many('request.order.line', 'order_id', string='Order Lines',
                                 states={'cancel': [('readonly', True)], 'confirmed': [('readonly', True)],  'approved': [('readonly', True) ], 'done': [('readonly', True) ]}, copy=True)

    note = fields.Text('Notes', )

    procurement_group_id = fields.Many2one('procurement.group', 'Procurement Group', copy=False)

    _defaults = {
        'employee_id': _employee_get,

    }

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('request.order') or 'New'

        result = super(RequestOrder, self).create(vals)
        return result

    @api.multi
    def unlink(self):
        for order in self:
            if order.state != 'draft':
                raise UserError(_('You can only delete draft request!'))
        return super(RequestOrder, self).unlink()

    @api.model
    def _prepare_procurement_group(self):
        return {'name': self.name, 'partner_id': self.partner_id.id}

    @api.multi
    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancel', 'confirmed'])
        orders.write({
            'state': 'draft',
            'procurement_group_id': False,
        })
        orders.mapped('order_line').mapped('procurement_ids').write({'request_line_id': False})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def action_approve(self):
        for order in self:
            order.state = 'approved'
            order.order_line._action_procurement_create()

        return True

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

    picking_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Picking associated to this sale')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')

    @api.multi
    @api.depends('procurement_group_id')
    def _compute_picking_ids(self):
        for order in self:
            order.picking_ids = self.env['stock.picking'].sudo().search(
                [('group_id', '=', order.procurement_group_id.id)]) if order.procurement_group_id else []
            order.delivery_count = len(order.picking_ids)

    @api.multi
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }

        pick_ids = sum([order.picking_ids.ids for order in self], [])

        if len(pick_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(map(str, pick_ids)) + "])]"
        elif len(pick_ids) == 1:
            form = self.env.ref('stock.view_picking_form', False)
            form_id = form.id if form else False
            result['views'] = [(form_id, 'form')]
            result['res_id'] = pick_ids[0]
        return result


class RequestOrderLine(models.Model):

    _name = 'request.order.line'
    _description = u'Request order line'

    _rec_name = 'name'
    _order = 'name ASC'

    order_id = fields.Many2one('request.order', string='Order Reference', required=True, ondelete='cascade', index=True,
                               copy=False)
    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True, ondelete='restrict', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True,
                                   default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)

    company_id = fields.Many2one(related='order_id.company_id', string='Company', store=True, readonly=True)
    order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Requstor')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], related='order_id.state', string='Order Status', readonly=True, copy=False, store=True, default='draft')

    procurement_ids = fields.One2many('procurement.order', 'request_line_id', string='Procurements')


    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
            vals['product_uom'] = self.product_id.uom_id

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            uom=self.product_uom.id
        )

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name

        self.update(vals)
        return {'domain': domain}

    @api.multi
    def unlink(self):
        if self.filtered(lambda x: x.state in ('approved', 'done')):
            raise UserError(
                _('You can not remove a reqeust order line.\nDiscard changes and try setting the quantity to 0.'))
        return super(RequestOrderLine, self).unlink()

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        self.ensure_one()
        return {
            'name': self.name or "Goods",
            'origin': self.order_id.name,
            'date_planned': datetime.strptime(self.order_id.date_order, DEFAULT_SERVER_DATETIME_FORMAT) ,
            'partner_dest_id': self.order_id.partner_id.id,
            'product_id': self.product_id.id,
            'product_qty': self.product_uom_qty,
            'product_uom': self.product_uom.id,
            'company_id': self.order_id.company_id.id,
            'warehouse_id': self.order_id.warehouse_id and self.order_id.warehouse_id.id or False,
            'location_id': self.order_id.partner_id.property_stock_customer.id,
            'group_id': group_id,
            'request_line_id': self.id
        }

    @api.multi
    def _action_procurement_create(self):
        """
        Create procurements based on quantity ordered. If the quantity is increased, new
        procurements are created. If the quantity is decreased, no automated action is taken.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        new_procs = self.env['procurement.order']  # Empty recordset
        for line in self:
            _logger.info('line product need_procurement :  %s' %line.product_id._need_procurement())

            if line.state != 'approved' or not line.product_id._need_procurement():
                _logger.info('no procurement')
                continue
            qty = 0.0
            for proc in line.procurement_ids:
                qty += proc.product_qty
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                continue

            if not line.order_id.procurement_group_id:
                vals = line.order_id._prepare_procurement_group()
                line.order_id.procurement_group_id = self.env["procurement.group"].create(vals)

            vals = line._prepare_order_line_procurement(group_id=line.order_id.procurement_group_id.id)
            vals['product_qty'] = line.product_uom_qty - qty
            new_proc = self.env["procurement.order"].sudo().create(vals)
            new_procs += new_proc
        new_procs.run()
        return new_procs


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'
    request_line_id = fields.Many2one('request.order.line', string='Request Order Line')
