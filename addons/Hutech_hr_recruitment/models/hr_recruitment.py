from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrRecruitment(models.Model):
    _inherit = 'hr.applicant'
    skills = fields.Char()
    submission_counts = fields.Integer(compute='_compute_submission_counts', string="Submission Count")
    applicants = fields.Integer(compute='_compute_applicants', string="applicants")
    prioritys = fields.Integer(compute='_compute_prioritys', string="prioritys")
    applicantss = fields.Integer(compute='_compute_applicantss', string="applicantss")
    applicantsss = fields.Integer(compute='_compute_applicantsss', string="applicantsss")


    @api.depends('job_id')
    def _compute_submission_counts(self):
        for record in self:
            submission_counts = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id)])
            record.submission_counts = submission_counts

    @api.depends('job_id')
    def _compute_applicants(self):
        for record in self:
            applicants = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id), ('stage_id.sequence', 'in', [2, 3])])
            record.applicants = applicants

    @api.depends('job_id')
    def _compute_prioritys(self):
        for record in self:
            prioritys = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id), ('priority', '>', 0)])
            record.prioritys = prioritys

    @api.depends('job_id')
    def _compute_applicantss(self):
        for record in self:
            applicantss = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id), ('stage_id.sequence', 'in', [4])])
            record.applicantss = applicantss

    @api.depends('job_id')
    def _compute_applicantsss(self):
        for record in self:
            applicantsss = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id), ('stage_id.sequence', 'in', [5])])
            record.applicantsss = applicantsss
