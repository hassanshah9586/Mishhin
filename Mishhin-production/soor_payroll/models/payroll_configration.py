# See LICENSE file for full copyright and licensing details
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalaryGrade(models.Model):
    _name = "salary.grade"
    _description = 'Salary Grade'

    name = fields.Integer(string="Grade")
    
    _sql_constraints = [
        ("grade_uniq", "unique(grade)", "Grade must be unique!"),
    ]


class KuwaitBasicSalary(models.Model):
    _name = "kuwait.basic.salary"
    _description = 'Kuwait Basic Salary'
    _rec_name = 'display_name'
    
    display_name = fields.Char(
        compute='_get_display_name', string='Display Name')
    name = fields.Selection([('minimum', 'Minimum-KWD'), ('midpoint', 'Midpoint-KWD'), ('maximum', 'Maximum-KWD')])
    line_ids = fields.One2many('kuwait.basic.salary.line', 'basic_salary_id', string="Salary Line")
    
    @api.depends('name')
    def _get_display_name(self):
        for rec in self:
            rec.display_name = dict(self._fields['name'].selection).get(rec.name)


class KuwaitBasicSalaryLine(models.Model):
    _name = "kuwait.basic.salary.line"
    _description = 'Kuwait Basic Salary Line'

    grade_id = fields.Many2one('salary.grade', string='Grade')
    value = fields.Float(string='Value')
    basic_salary_id = fields.Many2one('kuwait.basic.salary', string="Basic Salary")


class KuwaitHousingAllownce(models.Model):
    _name = "kuwait.housing.allowance"
    _description = 'Kuwait Housing Allowance'
    _rec_name = 'display_name'

    display_name = fields.Char(
        compute='_get_display_name', string='Display Name')
    name = fields.Selection(
        [('single', 'Single'), ('married', 'Married')], string='Marital Status')
    line_ids = fields.One2many(
        'kuwait.housing.allowance.line', 'basic_salary_id', string="Allowance Line")

    @api.depends('name')
    def _get_display_name(self):
        for rec in self:
            rec.display_name = dict(
                self._fields['name'].selection).get(rec.name)


class KuwaitHousingAllownceLine(models.Model):
    _name = "kuwait.housing.allowance.line"
    _description = 'Kuwait Housing Allowance Line'

    grade_id = fields.Many2one('salary.grade', string='Grade')
    value = fields.Float(string='Value')
    basic_salary_id = fields.Many2one(
        'kuwait.housing.allowance', string="Housing Allowance")


class KuwaitAcademicAllowance(models.Model):
    _name = "kuwait.academic.allowance"
    _description = 'Kuwait academic Allowance'
    _rec_name = 'display_name'

    display_name = fields.Char(
        compute='_get_display_name', string='Display Name')
    name = fields.Selection(
        [('high', 'High(Master/Doctoral)'), ('special', 'Special'), ('professional', 'Professional')], string='Academic Qualification')
    line_ids = fields.One2many(
        'kuwait.academic.allowance.line', 'basic_salary_id', string="Allowance Line")

    @api.depends('name')
    def _get_display_name(self):
        for rec in self:
            rec.display_name = dict(
                self._fields['name'].selection).get(rec.name)


class KuwaitAcademicAllowanceLine(models.Model):
    _name = "kuwait.academic.allowance.line"
    _description = 'Kuwait Academic Allowance Line'

    grade_id = fields.Many2one('salary.grade', string='Grade')
    value = fields.Float(string='Value')
    basic_salary_id = fields.Many2one(
        'kuwait.academic.allowance',
        string="Academic Allowance")


class PayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    timesheet_structure = fields.Boolean(string='Timesheet Based Structure', default=False,
                                         help='Flag Which says the Structure is based on Timesheets submitted by employee')


class HrContract(models.Model):
    _inherit = "hr.contract"

    car_allowance = fields.Float(string='Car Allowance')
    petrol_allowance = fields.Float(string='Petrol Allowance')
    transportation_allowance = fields.Float(string='Transportation Allowance')
    bussiness_allowance = fields.Float(string='Bussiness Trip Allowance')
    phone_allowance = fields.Integer(string='Phone Allowance')
    other_allowance = fields.Integer(string='Other Allowance')
    grade = fields.Many2one('salary.grade', string='Salary Grade')
    basic_salary = fields.Many2one(
        'kuwait.basic.salary', string="Basic Salary")
    housing_allowance = fields.Many2one(
        'kuwait.housing.allowance', string="Housing Allowance")
    academic_allowance = fields.Many2one(
        'kuwait.academic.allowance', string="Academic Allowance")
    # per_hour =  fields.Float('Per Hour')
    timesheet_payroll = fields.Boolean(
        string='Timesheet Based Payroll', default=True,
        help='Flag Which says the payroll is based on Timesheets submitted by employee')

    # @api.onchange('timesheet_payroll')
    # def onchange_timesheet_payroll(self):
    #     if self.timesheet_payroll:
    #         self.struct_id = False
    #         return {
    #             'domain': {
    #                 'struct_id': [('timesheet_structure', '=', True)]
    #             },
    #         }
    #     else:
    #         return {
    #             'domain': {'struct_id': []},
    #         }


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_hours = fields.Integer(
        string='Timesheet Hours',
        states={'done': [('readonly', True)]},
        help='Total Timesheet hours approved for employee.')
    total_hours = fields.Integer(
        string='Total Hours',
        states={'done': [('readonly', True)]},
        help='Total Hours By Working schedule')
    timesheet_payroll = fields.Boolean(
        related='contract_id.timesheet_payroll')

    def compute_timesheet_hours(self, contract_id, date_from, date_to):
        """
        Function which computes total hours, timesheethours, attendances, timehseet difference,
        :param employee_id:
        :param date_from:
        :param date_to:
        :return:  computed total timesheet hours within duration, total hours by working schedule
        """
        if not contract_id:
            return {}
        env = self.env
        employee_id = contract_id.employee_id
        timesheet_object = env['account.analytic.line']
        total_hours = 0.0
        timesheet_hours = timesheet_attendance = timesheet_difference = 0.0
        for line in self.worked_days_line_ids:
            total_hours += line.number_of_hours if line.code == 'WORK100' else 0.0
        sheets = timesheet_object.search([
            ('employee_id', '=', employee_id.id),
            ('date', '>=', date_from),
            ('date', '<=', date_to),
        ])
        print("sheets-------------->", sheets)
        if sheets:
            self.env.cr.execute("""
                SELECT
                    coalesce(sum(t.attendance), 0) AS total_attendance,
                    coalesce(sum(t.timesheet), 0) AS total_timesheet,
                    coalesce(sum(t.attendance), 0) - coalesce(sum(t.timesheet), 0) as total_difference
                FROM (
                    SELECT
                        -hr_attendance.id AS id,
                        resource_resource.user_id AS user_id,
                        hr_attendance.worked_hours AS attendance,
                        NULL AS timesheet,
                        hr_attendance.check_in::date AS date
                    FROM hr_attendance
                    LEFT JOIN hr_employee ON hr_employee.id = hr_attendance.employee_id
                    LEFT JOIN resource_resource on resource_resource.id = hr_employee.resource_id
                UNION ALL
                    SELECT
                        ts.id AS id,
                        ts.user_id AS user_id,
                        NULL AS attendance,
                        ts.unit_amount AS timesheet,
                        ts.date AS date
                    FROM
                        account_analytic_line
                    AS ts
                    WHERE
                        ts.project_id IS NOT NULL
                    AND
                        ts.date >= %s
                    AND
                        ts.date <= %s
                    AND
                        ts.employee_id =%s
                ) AS t
                
            """, (date_from, date_to, employee_id.id))
            data = self.env.cr.dictfetchall()
            for x in data:
                timesheet_hours = x.pop('total_timesheet')
                timesheet_attendance = x.pop('total_attendance')
                timesheet_difference = x.pop('total_difference')
        return {
            'timesheet_hours': timesheet_hours,
            'timesheet_attendance': timesheet_attendance,
            'timesheet_difference': timesheet_difference,
            'total_hours': total_hours,
        }

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        payslip = super(HrPayslip, self)._onchange_employee()
        if self.contract_id.timesheet_payroll:
            datas = self.compute_timesheet_hours(
                self.contract_id, self.date_from, self.date_to)
            self.timesheet_hours = datas.get('timesheet_hours') or 0.0
            self.total_hours = datas.get('total_hours') or 0.0
        return payslip
