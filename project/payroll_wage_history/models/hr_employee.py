import re
from odoo import fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    wage_history_count = fields.Integer(
        string='Wage history record',
        compute='_count_wage_history'
    )

    def _count_wage_history(self):
        PayrollWageHistory = self.env['payroll.wage.history']
        for rec in self:
            rec_count = PayrollWageHistory.search(
                [('employee_id', '=', rec.id)],
                count=True)
            rec.wage_history_count = rec_count
