from datetime import date
import datetime
from odoo import api, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.model
    def create(self, vals):
        result = super(HrContract, self).create(vals)
        self.env['payroll.wage.history'].create({
            'employee_id': result.employee_id.id,
            'contract_id': result.id,
            'responsible_id': result.hr_responsible_id.id,
            'current_payroll_wage': result.wage,
            'effective_date': date.today(),
        })
        return result

    def write(self, vals):
        current_wage = vals.get('wage')
        for rec in self:
            rec.env['payroll.wage.history'].create({
                'employee_id': rec.employee_id.id,
                'contract_id': rec.id,
                'responsible_id': rec.hr_responsible_id.id,
                'current_payroll_wage': current_wage,
                'previous_payroll_wage': rec.wage,
                'effective_date': date.today(),
            })
        return super(HrContract, self).write(vals)
    
