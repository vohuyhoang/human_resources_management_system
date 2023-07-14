# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _


class HrPayslipRun(models.Model):
    _name = 'hr.payslip.run'
    _inherit = ['hr.payslip.run', 'mail.thread', 'mail.activity.mixin']

    @api.one
    @api.depends('slip_ids')
    def _compute_amount(self):
        self.amount_total = sum(line.net_wage for line in self.slip_ids)

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_compute_amount',
                                   track_visibility='always')
    amount_total_vi = fields.Char(string='Total amount in words', store=True, readonly=True,
                                  compute='_compute_amount_total_vi',
                                  track_visibility='always')

    @api.multi
    def action_payslips_sent(self):
        self.ensure_one()
        self.slip_ids.force_payslip_sent()

    def convert_number_to_words(self, num):
        under_20 = ['Không', 'Một', 'Hai', 'Ba', 'Bốn', 'Năm', 'Sáu', 'Bảy', 'Tám', 'Chín', 'Mười', 'Mười một',
                    'Mười hai', 'Mười ba', 'Mười bốn', 'Mười lăm', 'Mười sáu', 'Mười bảy', 'Mười tám', 'Mười chín']
        tens = ['Hai mươi', 'Ba mươi', 'Bốn mươi', 'Năm mươi', 'Sáu mươi', 'Bảy mươi', 'Tám mươi', 'Chín mươi']
        above_100 = {100: 'Trăm', 1000: 'Ngàn', 1000000: 'Triệu', 1000000000: 'Tỷ'}

        if num < 20:
            return under_20[num]
        if num < 100:
            return tens[(int)(num / 10) - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])
        maxkey = max([key for key in above_100.keys() if key <= num])
        return self.convert_number_to_words((int)(num / maxkey)) + ' ' + above_100[maxkey] + (
            '' if num % maxkey == 0 else ' ' + self.convert_number_to_words(num % maxkey))

    @api.depends('amount_total')
    def _compute_amount_total_vi(self):
        self.amount_total_vi = (self.convert_number_to_words(int(self.amount_total)) + ' đồng')
