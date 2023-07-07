from odoo import models, fields

class CustomContract(models.Model):
    _inherit = 'hr.contract'

    custom_field = fields.Char('Custom Field')
    



