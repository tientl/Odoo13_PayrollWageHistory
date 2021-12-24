from datetime import datetime
from odoo import api, fields, models
import unicodedata


class PayrollWageHistory(models.Model):
    _name = 'payroll.wage.history'
    _description = 'Payroll wage history'
    _rec_name = 'revision'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        required=True,
        string='Employee name',
        index=True
    )
    contract_id = fields.Many2one(
        comodel_name='hr.contract',
        string='Contract',

    )
    # number_change = fields.Integer(
    #     string='Number of change',
    #     default=0)
    revision = fields.Char(string='Revision')
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
        related='employee_id.department_id',
        store=True
    )
    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job Title',
        related='employee_id.job_id',
        store=True
    )
    previous_payroll_wage = fields.Float(
        string='Previous payroll wage',
        digits=(16, 2))
    current_payroll_wage = fields.Float(
        string='Current payroll wage',
        digits=(16, 2))
    difference = fields.Float(
        string='Difference',
        compute='_different_compute',
        digits=(16, 2),
        store=True)
    percentage = fields.Float(
        compute='_different_compute',
        digits=(16, 2),
        store=True,
        string='Percentage(%)')
    effective_date = fields.Date(string='Effective date')
    responsible_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible person')
    id_desc = fields.Char(
        string='ID Desc',
        store=True,
        compute='_check_id_desc'
    )

    @api.depends('previous_payroll_wage', 'current_payroll_wage')
    def _different_compute(self):
        for rec in self:
            current = rec.current_payroll_wage
            previous = rec.previous_payroll_wage
            rec.difference = current - previous
            if not previous:
                rec.percentage = 0
            else:
                rec.percentage = 100 * (current-previous) / previous

    @api.depends('previous_payroll_wage', 'current_payroll_wage')
    def _check_id_desc(self):
        for rec in self:
            if rec.previous_payroll_wage < rec.current_payroll_wage:
                rec.id_desc = 'Increased wage'
            else:
                rec.id_desc = 'Decreased wage'

    # @api.depends('contract', 'number_change')
    # def _revision_compute(self):
    #     for rec in self:
    #         num = str(rec.number_change)
    #         year = str(datetime.now().year)
    #         contract = rec.contract
    #         rec.revision = contract + '-' + num + '-' + year

    @api.model
    def create(self, vals):
        get_contract = vals.get('contract_id')
        contract = self.env['hr.contract'].browse(get_contract)
        contract_name = contract.name
        i = contract.employee_id.wage_history_count
        year = datetime.now().year
        vals['revision'] = f'{contract_name}-{i}-{year}'
        return super(PayrollWageHistory, self).create(vals)

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        if self._context.get('highest_raise'):
            query = """
            select MAX(difference) from payroll_wage_history
            WHERE effective_date
            BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
            """
            cr = self.env.cr
            cr.execute(query)
            raise_difference = [x[0] for x in cr.fetchall()]
            args += [('difference', '=', raise_difference)]
        if self._context.get('no_raise'):
            query = '''
            select difference from payroll_wage_history
            where percentage = 0 and effective_date
            BETWEEN NOW() - INTERVAl'12 month' and now() '''
            cr = self.env.cr
            cr.execute(query)
            no_raise = [x[0] for x in cr.fetchall()]
            args += [('difference', '=', no_raise)]
        return super(PayrollWageHistory, self).search(
            args, offset=offset, limit=limit, order=order, count=count)

    def gender_change(self):
        for rec in self:
            if rec.employee_id.gender == 'male':
                return 'Ông'
            else:
                return 'Bà'

    def gender_change_english(self):
        for rec in self:
            if rec.employee_id.gender == 'male':
                return 'Mr'
            else:
                return 'Ms'

    def name_english(self):
        for rec in self:
            name = rec.employee_id.name
            name_eng = ''.join((
                c for c in unicodedata.normalize(
                    'NFD', name) if unicodedata.category(c) != 'Mn'))
        return name_eng
