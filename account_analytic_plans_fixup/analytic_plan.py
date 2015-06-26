# -*- coding: utf-8 -*-

import time
import logging 
from openerp.osv import fields, osv

class account_analytic_account(osv.osv):
    _inherit = "account.analytic.account"

    def _prepare_invoice_lines(self, cr, uid, contract, fiscal_position_id, context=None):
        context = context or {}

        invoice_lines = super(account_analytic_account, self)._prepare_invoice_lines(cr, uid, contract, fiscal_position_id, context=context)

        invoice = super(account_analytic_account, self)._prepare_invoice_data(cr, uid, contract, context=context)

        partner_id = invoice['partner_id']    

        for invoice_line in invoice_lines:   

            product = invoice_line[2]['product_id']       

            rec = self.pool.get('account.analytic.default').account_get(cr, uid, product, partner_id, uid,
                time.strftime('%Y-%m-%d'))

            if rec:
                invoice_line[2].update({'analytics_id': rec.analytics_id.id})
            else:
                invoice_line[2].update({'analytics_id': False})


        return invoice_lines