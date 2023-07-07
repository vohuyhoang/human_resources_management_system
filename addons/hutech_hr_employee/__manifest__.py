{
    'name': 'HUTECH HR Employee ',
    'depends': ['excel_import_export','hr','base'],
    'data': [
        'views/employee_views.xml',
        'views/employee_fields.xml',
        # 'views/ir_model_access.xml',
        'views/report_payslip_run_excel_templates.xml',
        'security/ir.model.access.csv',
       
    ],
    
    'installable': True,
    'application': True,
}
