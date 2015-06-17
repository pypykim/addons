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
from openerp.exceptions import Warning


class calendar_event(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def _create_resource_leaves(self, event):
        old_leaves = self.env['resource.calendar.leaves'].search([('calendar_event_id', '=', event.id)])
        _logger.info('remove existed resource leave for this event %s: %s' % (event, old_leaves))
        old_leaves.unlink()

        exists = self._exists_resource_leaves(event)
        if len(exists) > 0:
            raise Warning(
                'The resource have not full available for this time slot! \n Please choose another one, thanks.')

        resource_calendar_leaves_model = self.env['resource.calendar.leaves']

        leaves = resource_calendar_leaves_model.create(
            {
                'name': 'Meeting : {}'.format(event.name),
                'calendar_id': event.resource_ids.calendar_id.id,
                'resource_id': event.resource_ids.id,
                'date_from': event.start,
                'date_to': event.stop,
                'calendar_event_id': event.id,
            }
        )

        _logger.info('created leave %s for event %s' % (leaves, event))

        return leaves

    def _exists_resource_leaves(self, event):
        query = """
            SELECT id
            FROM resource_calendar_leaves
            WHERE
            resource_id = %s AND
            ((date_from  <=  %s  AND date_to  >=  %s )
            OR
            (date_from  >=  %s  AND date_from  <  %s )
            OR
            (date_to  >  %s  AND date_to  <=  %s )
            )


            """
        self._cr.execute(query, (
        event.resource_ids.id, event.start, event.stop, event.start, event.stop, event.start, event.stop))

        ids = []
        for id in self._cr.fetchall():
            ids.append(id)

        return ids

    @api.model
    def create(self, vals):
        """ Create the event then create resource leaves linked to the
        resources used by the event.
        """
        vals['allday'] = False
        event = super(calendar_event, self).create(vals)
        leaves = self._create_resource_leaves(event)
        return event

    @api.multi
    def write(self, vals):
        result = super(calendar_event, self).write(vals)

        leaves = self._create_resource_leaves(self)
        _logger.info('modified values: %s' % vals)
        _logger.info('event modified: %s' % self)

        return result

    resource_ids = fields.Many2one(
        'resource.resource',
        domain="[('display', '=', True)]",
        string='Room', required=True,
    )

    resource_calendar_leaves_ids = fields.Many2one(
        'resource.calendar.leaves',
        string='Room Calendar leaves', )
