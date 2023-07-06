from odoo import models, fields, api

class HrRecruitment(models.Model):
    _inherit = 'hr.applicant'
    skills = fields.Char()
    submission_counts = fields.Integer(compute='_compute_submission_counts', string="Submission Count")
    interview_counts = fields.Integer(compute='_compute_interview_counts', string="Interview Count")
    application_counts = fields.Integer(compute='_compute_application_counts', string="Application Count")
    interview_candidate_counts = fields.Integer(compute='_compute_interview_candidate_counts', string="Interview Candidate Count")
    interview_pass = fields.Boolean(string="Interview Pass")
    interview_pass_counts = fields.Integer(compute='_compute_interview_pass_counts', string="Interview Pass Count")
    hired_counts = fields.Integer(compute='_compute_hired_counts', string="Hired Count")

    @api.depends('job_id')
    def _compute_submission_counts(self):
        for record in self:
            submission_counts = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id)])
            record.submission_counts = submission_counts

    @api.depends('stage_id')
    def _compute_interview_counts(self):
        for record in self:
            interview_counts = len(record.stage_id)
            record.interview_counts = interview_counts

    @api.depends('job_id', 'stage_id')
    def _compute_application_counts(self):
        for record in self:
            application_counts = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id)])
            record.application_counts = application_counts

    @api.depends('job_id', 'stage_id')
    def _compute_interview_candidate_counts(self):
        for record in self:
            interview_candidate_counts = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id), ('stage_id', '!=', False)])
            record.interview_candidate_counts = interview_candidate_counts

    @api.depends('job_id')
    def _compute_interview_pass_counts(self):
        for record in self:
            interview_pass_counts = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id), ('interview_pass', '=', True)])
            record.interview_pass_counts = interview_pass_counts

    @api.depends('job_id')
    def _compute_hired_counts(self):
        for record in self:
            hired_counts = self.env['hr.applicant'].search_count([('job_id', '=', record.job_id.id),('stage_id', '=', 'hired')])
            record.hired_counts = hired_counts

    # @api.depends('state')
    # def _compute_official_contract_count(self):
    #     for applicant in self:
    #         official_contract_count = self.env['hr.contract'].search_count([('employee_id', '=', applicant.id), ('state', '=', 'open')])
    #         applicant.official_contract_count = official_contract_count