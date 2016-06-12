# -*- coding: utf-8 -*-

from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class HrAttendacne(models.Model):
    _inherit = 'hr.attendance'

    calendar_event_id = fields.Many2one(comodel_name="calendar.event", string="Meeting", required=False, )
    latitude = fields.Char(string="Latitude", required=False, )
    longitude = fields.Char(string="Longitude", required=False, )


class CalendarEventCICO(models.Model):
    _inherit = 'calendar.event'

    cico_ids = fields.One2many(comodel_name="hr.attendance", inverse_name="calendar_event_id", string="Check In/Out",
                               required=False, )

    @api.multi
    def event_cico(self):
        _logger.info('-----id is %s -----' %self.id)
        return {
            'type': 'ir.actions.client',
            'tag': 'calendar_event_cico_check',
            'target': 'new',
            'params': {'event_id': self.id}
        }
