# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class DocumentCollection(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'document.collection'
    _description = u'Document collection'

    _rec_name = 'name'
    _order = 'name ASC'

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

    usage = fields.Text(
        string='Usage',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        translate=True
    )

    attachments = fields.One2many(
        string='Documents',
        comodel_name='ir.attachment',
        compute='_compute_documents',
    )

    def attachment_tree_view(self, cr, uid, ids, context):
        domain = [
            '&', ('res_model', '=', 'document.collection'), ('res_id', 'in', ids),
        ]
        res_id = ids and ids[0] or False
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
        }

    @api.multi
    def _compute_documents(self):
        cr, uid, context = self._cr, self._uid, self._context
        model = self._name
        ir_attachment_obj = self.env["ir.attachment"]
        res = {}
        for res_id in self.ids:
            res[res_id] = ir_attachment_obj.search([('res_id', '=', res_id), ('res_model', '=', model)])
        for attach in self:
            if attach.id:
                attach.attachments = res[attach.id]
