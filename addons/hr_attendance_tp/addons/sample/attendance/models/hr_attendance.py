import calendar,locale
from odoo import models, fields, api, exceptions, _
from datetime import datetime, time, timedelta
import pytz
import logging
_logger = logging.getLogger(__name__)


class CustomHrAttendance(models.Model):
    _inherit = "hr.attendance"


    late_minutes = fields.Integer(
        string='Late Minutes', compute='_compute_late_minutes')

    def _compute_late_minutes(self):
        target_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        target_time = datetime.combine(datetime.now().date(), time(hour=8, minute=0, second=0))
        target_time = target_timezone.localize(target_time)
        
        for attendance in self:
            if attendance.check_in:
                check_in_time = fields.Datetime.from_string(attendance.check_in)
                check_in_time = pytz.UTC.localize(check_in_time)
                check_in_time = check_in_time.astimezone(target_timezone)

                check_in_hour = check_in_time.time()
                target_hour = target_time.time()
                
                if check_in_hour > target_hour:
                    diff = datetime.combine(datetime.min.date(), check_in_hour) - datetime.combine(datetime.min.date(), target_hour)
                    diff_minutes = int(diff.total_seconds() // 60)
                    attendance.late_minutes = diff_minutes
                else:
                    attendance.late_minutes = 0

    early_minutes = fields.Integer(string='Early Minutes', compute='_compute_early_minutes')

    def _compute_early_minutes(self):
        target_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        target_time = datetime.combine(datetime.now().date(), time(hour=17, minute=0, second=0))
        target_time = target_timezone.localize(target_time)

        for attendance in self:
            if attendance.check_out:
                check_out_time = fields.Datetime.from_string(attendance.check_out)
                check_out_time = pytz.UTC.localize(check_out_time)
                check_out_time = check_out_time.astimezone(target_timezone)

                check_out_hour = check_out_time.time()
                target_hour = target_time.time()

                if check_out_hour < target_hour:
                    diff = datetime.combine(datetime.min.date(), target_hour) - datetime.combine(datetime.min.date(), check_out_hour)
                    diff_minutes = int(diff.total_seconds() // 60)
                    attendance.early_minutes = diff_minutes
                else:
                    attendance.early_minutes = 0


    total_late_minutes = fields.Integer(string='Total Late Minutes', compute='_compute_total_late_minutes')
    total_early_minutes = fields.Integer(string='Total Early Minutes', compute='_compute_total_early_minutes')

    @api.depends('employee_id.attendance_ids.late_minutes')
    def _compute_total_late_minutes(self):
        for record in self:
            record.total_late_minutes = sum(record.employee_id.attendance_ids.mapped('late_minutes'))

    @api.depends('employee_id.attendance_ids.early_minutes')
    def _compute_total_early_minutes(self):
        for record in self:
            record.total_early_minutes = sum(record.employee_id.attendance_ids.mapped('early_minutes'))


    day_of_week = fields.Char(string='Thứ trong tuần', compute='_compute_day_of_week', store=True)

    @api.depends('check_in')
    def _compute_day_of_week(self):
            for attendance in self:
                if attendance.check_in:
                    check_in_date = fields.Datetime.from_string(attendance.check_in)
                    day_of_week = calendar.day_name[check_in_date.weekday()]
                    attendance.day_of_week = day_of_week
    # @api.depends('check_in')
    # def _compute_day_of_week(self):
    #     # Set the locale to Vietnamese
    #     locale.setlocale(locale.LC_TIME, 'vi_VN.utf8')

    #     for attendance in self:
    #         if attendance.check_in:
    #             check_in_date = fields.Datetime.from_string(attendance.check_in)
    #             day_of_week = check_in_date.strftime('%A')  # %A: Full weekday name
    #             attendance.day_of_week = day_of_week


    late_count = fields.Integer(string='Late Count', compute='_compute_late_count')
    early_count = fields.Integer(string='Early Count', compute='_compute_early_count')


    def _compute_late_count(self):
        for attendance in self:
            attendance.late_count = 1 if attendance.late_minutes > 0 else 0

    def _compute_early_count(self):
        for attendance in self:
                attendance.early_count = 1 if attendance.early_minutes > 0 else 0


    total_late_count = fields.Integer(string='Total Late Count', compute='_compute_total_late_count')

    @api.depends('late_count')
    def _compute_total_late_count(self):
        for record in self:
            record.total_late_count = sum(record.employee_id.attendance_ids.mapped('late_count'))


    total_early_count = fields.Integer(string='Total Early Count', compute='_compute_total_early_count')

    @api.depends('early_count')
    def _compute_total_early_count(self):
        for record in self:
            record.total_early_count = sum(record.employee_id.attendance_ids.mapped('early_count'))

    
   
       # _logger.info("Thời gian trễ:", late_minutes, "phút")