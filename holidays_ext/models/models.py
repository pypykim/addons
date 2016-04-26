# -*- coding: utf-8 -*-

import calendar
import datetime
from datetime import date
import logging
import math
import time
from operator import attrgetter
from werkzeug import url_encode

from dateutil.relativedelta import relativedelta

from openerp.exceptions import UserError, AccessError
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class res_company(models.Model):
    _inherit = ['res.company']

    resource_calendar = fields.Many2one(
        string='Resource Calendar',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='resource.calendar',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

class hr_holidays(models.Model):
    _inherit = ['hr.holidays']

    def _get_number_of_days(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.datetime.strptime(date_to, DATETIME_FORMAT)
        calendar = self.env['res.users'].browse(self.env.uid).company_id.resource_calendar
        _logger.info('working hours calenadr %s' % calendar)
        working_hours = self.pool.get('resource.calendar').get_working_hours(self.env.cr, 1, calendar.id, from_dt, to_dt, context=self.env.context)
        # working_hours = self.env['resource.calendar'].get_working_hours(calendar.id, from_dt, to_dt, context=self.env.context)
        _logger.info('working hours %s' % working_hours)
        if working_hours and working_hours > 0:
            diff_day = float(working_hours) / 8
        else:
            diff_day = 0
        return diff_day

    @api.multi
    def onchange_date_from(self, date_to, date_from):
        """
        If there are no date set for date_to, automatically set one 8 hours later than
        the date_from.
        Also update the number_of_days.
        """
        # date_to has to be greater than date_from
        if (date_from and date_to) and (date_from > date_to):
            raise UserError(_('The start date must be anterior to the end date.'))

        result = {'value': {}}

        # No date_to set so far: automatically compute one 8 hours later
        if date_from and not date_to:
            date_to_with_delta = datetime.datetime.strptime(date_from, tools.DEFAULT_SERVER_DATETIME_FORMAT) + datetime.timedelta(hours=8)
            result['value']['date_to'] = str(date_to_with_delta)

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            diff_day = self._get_number_of_days(date_from, date_to)
            result['value']['number_of_days_temp'] = diff_day
        else:
            result['value']['number_of_days_temp'] = 0

        return result

    @api.multi
    def onchange_date_to(self, date_to, date_from):
        """
        Update the number_of_days.
        """
        # date_to has to be greater than date_from
        if (date_from and date_to) and (date_from > date_to):
            raise UserError(_('The start date must be anterior to the end date.'))

        result = {'value': {}}

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            diff_day = self._get_number_of_days(date_from, date_to)
            result['value']['number_of_days_temp'] = diff_day
        else:
            result['value']['number_of_days_temp'] = 0
        return result
