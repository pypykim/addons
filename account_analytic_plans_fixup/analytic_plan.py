from openerp import fields, models


class accountInvoice(models.Model):
    _inherit = 'account.invoice'


class accountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'


class accountAnalyticPlanInstance(models.Model):
    _inherit = 'account.analytic.plan.instance'
