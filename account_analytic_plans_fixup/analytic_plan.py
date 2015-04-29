
import time

from openerp.osv import fields, osv

class account_analytic_account(osv.osv):
    _inherit = "account.analytic.account"

    def _prepare_invoice_lines(self, cr, uid, contract, context=None):
        context = context or {}
        invoice = super(account_analytic_account, self)._prepare_invoice_data(cr, uid, contract, context=context)

        fiscal_position_id = invoice['fiscal_position']
        partner_id = invoice['partner_id']

        invoice_line = super(account_analytic_account, self)._prepare_invoice_lines(cr, uid, contract,
            fiscal_position_id,
            context=context)

        product = invoice_line['product_id']

        rec = self.pool.get('account.analytic.default').account_get(cr, uid, product, partner_id, uid,
            time.strftime('%Y-%m-%d'))

        if rec:
            invoice_line.update({'account_analytic_id': rec.analytic_id.id})
            invoice_line.update({'analytics_id': rec.analytics_id.id})
        else:
            invoice_line.update({'account_analytic_id': False})
            invoice_line.update({'analytics_id': False})
            
        return invoice_line