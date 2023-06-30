{
    'name': 'Employees',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 75,
    'summary': 'Centralize employee information',
    'description': "",
    'website': 'https://www.odoo.com/page/employees',
    'images': [
        'images/hr_department.jpeg',
        'images/hr_employee.jpeg',
        'images/hr_job_position.jpeg',
        'static/src/img/default_image.png',
    ],
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'excel_import_export',
        'web',
    ],
    'data': [
        'views/employee_views.xml',
        'views/employee_fields.xml',
        # 'views/reporting.xml',
        'views/ir_model_access.xml',
        'views/report_payslip_run_excel_templates.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/hr_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
    'license': 'LGPL-3',
}

