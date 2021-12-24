
{
    'name': 'Payroll Wage History',
    'version': '1.0',
    'category': 'Payroll',
    'description': """
    Model thử nghiệm
    """,
    'depends': ['hr_contract', 'report_py3o'],
    'data': [
        # data
        'data/py3o_template_data.xml',
        # access right
        'security/ir.model.access.csv',
        # report
        'report/py3o/report_py3o.xml',
        'report/qweb/report_qweb.xml',
        'report/qweb/templates/report_salary_adjustment_form.xml',
        'report/xlsx/report_xlsx.xml',
        # wizard
        'wizard/reporting_wizard.xml',
        # views
        'view/hr_employee_view.xml',
        'view/hr_contract_view.xml',
        'view/payroll_wage_history_view.xml',
        # Menu
        'menu/payroll_wage_history_menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True
}
