# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _


class HrPayslip(models.Model):
    _name = 'hr.payslip'
    _inherit = ['hr.payslip', 'mail.thread']

    currency_id = fields.Many2one(related='contract_id.currency_id')
    basic_wage = fields.Monetary(compute='_compute_basic_net')
    net_wage = fields.Monetary(compute='_compute_basic_net')

    def _compute_basic_net(self):
        for payslip in self:
            payslip.basic_wage = payslip._get_salary_line_total('BASIC')
            payslip.net_wage = payslip._get_salary_line_total('NET')

    def _get_salary_line_total(self, code):
        lines = self.line_ids.filtered(lambda line: line.code == code)
        return sum([line.total for line in lines])

    @api.multi
    def action_payslip_sent(self):
        self.ensure_one()
        template = self.env.ref('hr_payroll_vn.email_template_edi_payslip', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='hr.payslip',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            custom_layout="mail.mail_notification_light",
            mark_so_as_sent=True
        )
        return {
            'name': _('Send PaySlip'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.one
    def force_payslip_sent(self):
        composer_obj = self.env['mail.compose.message']
        email_act = self.action_payslip_sent()
        if email_act and email_act.get('context'):
            composer_values = {}
            email_ctx = email_act['context']
            composer_values.update(composer_obj.onchange_template_id(
                template_id=email_ctx.get('default_template_id'),
                composition_mode=email_ctx.get('default_composition_mode'),
                model=email_ctx.get('default_model'),
                res_id=email_ctx.get('default_res_id')
            )['value'])
            if not composer_values.get('email_from'):
                composer_values['email_from'] = self.company_id.email
            composer_obj = composer_obj.with_context(
                default_model=email_ctx.get('default_model'),
                default_res_id=email_ctx.get('default_res_id'),
                default_use_template=email_ctx.get('default_use_template'),
                default_template_id=email_ctx.get('default_template_id'),
                default_composition_mode=email_ctx.get('default_composition_mode'),
                mark_so_as_sent=email_ctx.get('mark_so_as_sent')
            )
            composer = composer_obj.create(composer_values)
            composer.send_mail()
        return True
