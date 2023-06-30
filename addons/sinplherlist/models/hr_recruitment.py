from odoo import fields, models, api, _

class Hr_Recruitment(models.Model):
    _inherit = 'hr.applicant'

    Skills = fields.Char()
