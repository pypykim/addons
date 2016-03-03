# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    @api.model
    def _get_delivery_type(self):
        return [
            ('fixed', 'Fixed Price'),
            ('base_on_rule', 'Based on Rules')
        ]

    _delivery_type_selection = lambda self, *args, **kwargs: self._get_delivery_type(*args, **kwargs)

    delivery_type = fields.Selection(_delivery_type_selection, string='Price Computation', default='fixed', required=True)
