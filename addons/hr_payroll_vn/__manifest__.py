{
    'name': 'Vietnam HR Payroll',
    'depends': ['excel_import_export',
                'hr_payroll'],
    'data': [
        'views/hr_payslip_views.xml',
        'views/report_payslip_run_templates.xml',
        'views/hr_payslip_run_views.xml',
        'views/hr_payroll_run_report.xml',
        'views/report_payslip_run_excel_templates.xml',
        'data/mail_template_data.xml'
    ]
}