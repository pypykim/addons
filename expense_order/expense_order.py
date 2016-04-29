# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _
from openerp.exceptions import UserError

import openerp.addons.decimal_precision as dp


class ExpenseOrder(models.Model):
    _name = "expense.order"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Expense Order"

    @api.depends('expense_line.total_amount')
    def _compute_amount(self):
        for order in self:
            untaxed_amount = total_amount = 0.0
            for line in order.expense_line:
                untaxed_amount += line.untaxed_amount
                total_amount += line.total_amount

            untaxed_amount = order.currency_id.round(untaxed_amount)
            total_amount = order.currency_id.round(total_amount)
            tax_amount = total_amount - untaxed_amount

            order.update({
                'untaxed_amount': untaxed_amount,
                'tax_amount': tax_amount,
                'total_amount': total_amount,
            })

    name = fields.Char(string=u'报销名称', readonly=True, required=True, states={'draft': [('readonly', False)]})
    date = fields.Date(readonly=True, states={'draft': [('readonly', False)]}, default=fields.Date.context_today,
                       string=u"日期")
    employee_id = fields.Many2one('hr.employee', string=u'员工', required=True, readonly=True,
                                  states={'draft': [('readonly', False)]},
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)],
                                                                                      limit=1))
    company_id = fields.Many2one('res.company', string=u'公司', readonly=True, states={'draft': [('readonly', False)]},
                                 default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', string=u'货币', readonly=True, states={'draft': [('readonly', False)]},
                                  default=lambda self: self.env.user.company_id.currency_id)
    department_id = fields.Many2one('hr.department', string=u'部门',
                                    states={'post': [('readonly', True)], 'done': [('readonly', True)]},
                                    related='employee_id.department_id')
    analytic_account_id = fields.Many2one('account.analytic.account', string=u'项目',
                                          states={'post': [('readonly', True)], 'done': [('readonly', True)]},
                                          oldname='analytic_account', domain=[('account_type', '=', 'normal')])
    description = fields.Text()
    payment_mode = fields.Selection([("own_account", u"员工（报销）"), ("company_account", u"公司")], default='own_account',
                                    states={'done': [('readonly', True)], 'post': [('readonly', True)]}, string=u"付款")
    journal_id = fields.Many2one('account.journal', string=u'分类账',
                                 states={'done': [('readonly', True)], 'post': [('readonly', True)]},
                                 default=lambda self: self.env['account.journal'].search([('type', '=', 'purchase')],
                                                                                         limit=1),
                                 help="The journal used when the expense is done.")
    bank_journal_id = fields.Many2one('account.journal', string='存款日志',
                                      states={'done': [('readonly', True)], 'post': [('readonly', True)]},
                                      default=lambda self: self.env['account.journal'].search(
                                          [('type', 'in', ['cash', 'bank'])], limit=1),
                                      help="The payment method used when the expense is paid by the company.")
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    total_amount = fields.Float(string=u'总计', store=True, compute='_compute_amount', digits=dp.get_precision('Account'))
    tax_amount = fields.Float(string='Tax', store=True, compute='_compute_amount', digits=dp.get_precision('Account'))
    untaxed_amount = fields.Float(string='Subtotal', store=True, compute='_compute_amount',
                                  digits=dp.get_precision('Account'))
    expense_line = fields.One2many("hr.expense", 'order_id', string=u'费用明细')

    state = fields.Selection([('draft', '草稿'),
                              ('submit', '提交'),
                              ('approve', '批准'),
                              ('post', '等待付款'),
                              ('done', '已付'),
                              ('cancel', '拒绝')
                              ], string=u'状态', index=True, readonly=True, track_visibility='onchange', copy=False,
                             default='draft', required=True,
                             help='When the expense request is created the status is \'To Submit\'.\n It is submitted by the employee and request is sent to manager, the status is \'Submitted\'.\
        \nIf the manager approve it, the status is \'Approved\'.\n If the accountant genrate the accounting entries for the expense request, the status is \'Waiting Payment\'.')

    @api.multi
    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'expense.order'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.department_id = self.employee_id.department_id

    @api.model
    def create(self, vals):

        for ve in vals.get('expense_line', None):
            e = ve[2]
            product = self.env['product.product'].browse(e['product_id'])

            e['name'] = vals['name'] + '_' + product[0].name
            e['date'] = vals['date']
            e['employee_id'] = vals['employee_id']
            e['company_id'] = vals['company_id']
            e['currency_id'] = vals['currency_id']
            e['department_id'] = vals['department_id']
            e['payment_mode'] = vals['payment_mode']
            e['journal_id'] = vals['journal_id']
            e['bank_journal_id'] = vals['bank_journal_id']
            e['analytic_account_id'] = vals['analytic_account_id']

        return super(ExpenseOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        e = {}

        if vals.get('employee_id', False):
            e['employee_id'] = vals['employee_id']
        if vals.get('company_id', False):
            e['company_id'] = vals['company_id']
        if vals.get('currency_id', False):
            e['currency_id'] = vals['currency_id']
        if vals.get('department_id', False):
            e['department_id'] = vals['department_id']
        if vals.get('payment_mode', False):
            e['payment_mode'] = vals['payment_mode']
        if vals.get('journal_id', False):
            e['journal_id'] = vals['journal_id']
        if vals.get('bank_journal_id', False):
            e['bank_journal_id'] = vals['bank_journal_id']
        if vals.get('analytic_account_id', False):
            e['analytic_account_id'] = vals['analytic_account_id']

        for l in self.expense_line:
            if vals.get('name', False):
                n = {}
                product = self.env['product.product'].browse(e.product_id.id)
                n['name'] = vals['name'] + '_' + product[0].name
                l.write(n)
            if e:
                l.write(e)

        return super(ExpenseOrder, self).write(vals)

    def _get_product_tags(self, product_analytic_id):
        aaa = self.env['account.analytic.account'].browse(product_analytic_id)
        prod_tags = [t.id for t in aaa.tag_ids]
        return prod_tags

    def _get_project_tags(self, project_id):
        project = self.env['project.project'].browse(project_id)
        tags = project.tag_ids
        domain = [['tag_ids', '=', t.name] for t in tags]
        aaa = self.env['account.analytic.account'].search(domain)
        proj_tags = []
        for a in aaa:
            a_tags = [t.id for t in a.tag_ids]
            proj_tags.append((a.id, a_tags))
        return proj_tags

    def project_analyze_account(self, product_analytic_id, project_id):
        prod_tags = self._get_product_tags(product_analytic_id)
        if not prod_tags:
            return False
        proj_tags = self._get_project_tags(project_id)
        pk, max = 0, 0
        for proj_tag in proj_tags:
            tag_and = list(set(prod_tags).intersection(set(proj_tag[1])))
            if len(tag_and) > max:
                max = len(tag_and)
                pk = proj_tag[0]
        return pk

    @api.multi
    def submit_expenses(self):
        if any(expense.state != 'draft' for expense in self):
            raise UserError(_("You can only submit draft expenses!"))
        self.write({'state': 'submit'})
        self.expense_line.write({'state': self.state})

        # here assign the analyze account for each product
        # if no project, do noting
        # if not self.project_id:
        #     return

        # for l in self.expense_line:
        #     analytic_account_id = self.project_analyze_account(l.product_id.analytic_account_id.id,self.project_id.id)
        #     if not analytic_account_id:
        #         raise UserError(u'对应项目的分析账号没有维护好！')

        #     l.write({'analytic_account_id':analytic_account_id})

    @api.multi
    def approve_expenses(self):
        self.write({'state': 'approve'})
        self.expense_line.write({'state': self.state})

    @api.multi
    def refuse_expenses(self, reason):
        self.write({'state': 'cancel'})
        self.expense_line.write({'state': self.state})
        if self.employee_id.user_id:
            body = (_(
                "Your Expense %s has been refused.<br/><ul class=o_timeline_tracking_value_list><li>Reason<span> : </span><span class=o_timeline_tracking_value>%s</span></li></ul>") % (
                    self.name, reason))
            self.message_post(body=body, partner_ids=[self.employee_id.user_id.partner_id.id])

    @api.multi
    def paid_expenses(self):
        self.write({'state': 'done'})
        self.expense_line.write({'state': self.state})

    @api.multi
    def reset_expenses(self):
        return self.write({'state': 'draft'})
        self.expense_line.write({'state': self.state})

    @api.multi
    def action_move_create(self):
        self.expense_line.write({'state': self.state})
        for e in self.expense_line:
            e.action_move_create()

            if e.state == 'done':
                self.write({'state': 'done'})

        self.write({'state': 'post'})

    @api.multi
    def action_check(self):
        checks = []
        for e in self.expense_line:
            checks.append(e.state)

        if 'post' not in checks:
            self.write({'state': 'done'})

    @api.multi
    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'expense.order'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'expense.order', 'default_res_id': self.id}
        return res


class HrExpense(models.Model):
    _inherit = "hr.expense"

    order_id = fields.Many2one('expense.order', string='expense order')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if not self.name:
                self.name = self.product_id.display_name or ''
            self.unit_amount = self.env['product.template']._price_get(self.product_id, 'standard_price')[
                self.product_id.id]
            self.product_uom_id = self.product_id.uom_id
            self.tax_ids = self.product_id.supplier_taxes_id
            # self.analytic_account_id = self.product_id.analytic_account_id
