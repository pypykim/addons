# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
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

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT

from openerp import models, fields, api


class calendar_event(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def _create_resource_leaves(self, event):
        resource_calendar_leaves_model = self.env['resource.calendar.leaves']

        leaves = resource_calendar_leaves_model.create(
            {
                'name': 'Meeting : {}'.format(event.name),
                'calendar_id': event.resource_ids.resource_calendar.id,
                'resource_id': event.resource_ids.id,
                'date_from': event.start,
                'date_to': event.stop,
                'calendar_event_id': event.id,
            }
        )

        return leaves

    def _exists_resource_leaves(self, event):
        domain = [
            ('calendar_id', '=', event.resource_ids.resource_calendar.id),
            ('resource_id', '=', event.resource_ids.id),

            '|', ('date_from', '>=', event.start),
            '|', ('date_from', '<=', event.stop),

            ('date_to', '>=', event.start),
            ('date_to', '<=', event.stop),

        ]

        return self.env['resource.calendar.leaves'].search(domain)

    @api.model
    def create(self, vals):
        """ Create the event then create resource leaves linked to the
        resources used by the event.
        """
        event = super(calendar_event, self).create(vals)
        self._create_resource_leaves(event)
        return event

    @api.multi
    def write(self, vals):
        return super(calendar_event, self).write(vals)

    resource_ids = fields.Many2one(
        'resource.resource',
        domain="[('display', '=', True)]",
        string='Resources'
    )

    resource_calendar_leaves_ids = fields.Many2one(
        'resource.calendar.leaves',
        string='Resources Calendar leaves'
    )
