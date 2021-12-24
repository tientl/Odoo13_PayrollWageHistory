from odoo import models, fields


class PayrollWageHistoryWizard(models.TransientModel):
    _name = "payroll.wage.history.wizard"
    _description = "Payroll Wage History Wizard"

    employee_ids = fields.Many2many(comodel_name='hr.employee')
    job_ids = fields.Many2many(comodel_name='hr.job')
    department_ids = fields.Many2many(comodel_name='hr.department')
    wage_history_ids = fields.Many2many(
        comodel_name='payroll.wage.history',
        string='Payroll wage history',
        request=True)
    from_date = fields.Date(string="From Date", request=True)
    to_date = fields.Date(
        string="To Date",
        required=True,
        default=fields.Date.context_today)

    def filter_wizard_action(self):
        search = []
        if self.from_date:
            search.append(('effective_date', '>=', self.from_date))
        search.append(('effective_date', '<=', self.to_date))
        if self.employee_ids.ids:
            search.append(('employee_id', 'in', self.employee_ids.ids))
        if self.department_ids.ids:
            search.append(('department_id', 'in', self.department_ids.ids))
        if self.job_ids.ids:
            search.append(('job_id', 'in', self.job_ids.ids))
        wage_history = self.env[
            'payroll.wage.history'].search(search)
        self.wage_history_ids = wage_history.ids
        return {
            'name': 'Wage history Wizard',
            "views": [(False, "form")],
            'res_model': self._name,
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
