# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _


class HrPayslipRun(models.Model):
    _name = 'hr.payslip.run'
    _inherit = 'hr.payslip.run'

    @api.multi
    def action_payslips_sent(self):
        self.ensure_one()
        self.slip_ids.force_payslip_sent()
