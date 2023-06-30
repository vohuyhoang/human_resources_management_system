from odoo import fields, models, api
from openpyxl.styles import colors, Alignment, Border, Side, Font


class XLSXStyles(models.AbstractModel):
    _inherit = ['xlsx.styles']

    @api.model
    def get_openpyxl_styles(self):
        styles = super(XLSXStyles, self).get_openpyxl_styles()
        styles['align']['middle_vertical'] = Alignment(vertical='center')
        styles['font']['times_new_roman'] = Font(name="Times New Roman")
        return styles


class CustomHrHolidays(models.Model):
    _inherit = 'hr.leave'

