{
    'name': 'My Leave',
    'depends': ['excel_import_export','hr_holidays','base'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_holiday_view.xml',
    ],
    'installable': True,
    'application': True,
}
