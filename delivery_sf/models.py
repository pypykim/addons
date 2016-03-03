# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DeliveryCarrierSF(models.Model):
    _inherit = 'delivery.carrier'

    ''' A Shipping Provider

    In order to add your own external provider, follow these steps:

    1. Create your model MyProvider that _inherit 'delivery.carrier'
    2. Extend the selection of the field "delivery_type" with a pair
       ('<my_provider>', 'My Provider')
    3. Add your methods:
       <my_provider>_get_shipping_price_from_so
       <my_provider>_send_shipping
       <my_provider>_open_tracking_page
       <my_provider>_cancel_shipment
       (they are documented hereunder)
    '''

    def _get_delivery_type(self):
        delivery_type = super(DeliveryCarrierSF, self)._get_delivery_type()
        delivery_type.append(('sf', 'SF Express'))
        return delivery_type

    def sf_get_shipping_price_from_so(self, order):
        return [0.0]

    def sf_send_shipping(self, pickings):
        pass

    def sf_get_tracking_link(self, pickings):
        pass

    def sf_cancel_shipment(self, pickings):
        pass
