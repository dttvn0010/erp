from django.db import models
from django.contrib.auth.models import Group
from core.models import User, Company
from accounting.models import Invoice
from core.constants import BaseStatus

from .constants import (
    WorkShiftStatus,
    LeaveDayStatus, 
    PayrollStatus, 
    PrepaidStatus, 
    TaskStatus
)

# Create your models here.
class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    parent = models.ForeignKey('Department', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    
    manager = models.ForeignKey('Employee', 
        blank=True, null=True,
        related_name='manage_department', 
        on_delete=models.PROTECT
    )

    status = models.CharField(choices=BaseStatus.choices(), 
                default=BaseStatus.DRAFT.name,
                max_length=50)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    department = models.ForeignKey(Department, 
                    blank=True, null=True, on_delete=models.PROTECT)

    name = models.CharField(max_length=200)
    leader = models.ForeignKey('Employee', related_name='lead_teams', on_delete=models.PROTECT)
    members = models.ManyToManyField('Employee', related_name='member_teams')

    status = models.CharField(choices=BaseStatus.choices(), 
                    default=BaseStatus.DRAFT.name,
                    max_length=50)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    
    department = models.ForeignKey(Department, 
        related_name='department_employees',
        blank=True, null=True, 
        on_delete=models.PROTECT
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    code = models.CharField(max_length=100, unique=True)

    bank_acount = models.ForeignKey('accounting.BankAccount', 
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    direct_manager = models.ForeignKey('Employee', 
        blank=True, null=True,
        on_delete=models.PROTECT,
    )

    no_financial_dependents = models.IntegerField()
    leave_days_per_year = models.IntegerField()

    def __str__(self):
        return self.user.display

class Task(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    
    assignee = models.ForeignKey(Employee, 
        related_name='assigned_tasks', 
        on_delete=models.PROTECT
    )

    assigner = models.ForeignKey(Employee, 
        related_name='created_tasks', 
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=200)
    deadline = models.DateTimeField(blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TaskUpdate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    note = models.CharField(max_length=500, blank=True)
    status = models.CharField(choices=TaskStatus.choices(), max_length=50)
    update_person = models.ForeignKey(User, on_delete=models.PROTECT)
    update_date = models.DateTimeField(auto_now_add=True)

class CheckInMachine(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    location = models.CharField(max_length=200)
    ip = models.CharField(max_length=100)
    description = models.CharField(max_length=500, verbose_name='Mô tả', blank=True)
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=BaseStatus.choices(), 
                default=BaseStatus.DRAFT.name,
                max_length=50)

    def __str__(self):
        return self.ip

class EmployeeCheckIn(models.Model):
    machine = models.ForeignKey(CheckInMachine, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField()

class LeaveDayPeriod(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    start_date = models.IntegerField()
    end_date = models.IntegerField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=BaseStatus.choices(), 
                    default=BaseStatus.DRAFT.name,
                    max_length=50)

class EmployeeLeaveDayQuota(models.Model):
    period = models.ForeignKey(LeaveDayPeriod, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    original_qty = models.IntegerField()
    remain_qty = models.IntegerField()

class EmployeeLeaveDay(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    qty = models.FloatField()
    paid = models.BooleanField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=LeaveDayStatus.choices(), 
                    default=LeaveDayStatus.DRAFT.name,
                    max_length=50)

class IncomeTaxPolicy(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    base_salary = models.IntegerField()
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class IncomeTaxLevel(models.Model):
    policy = models.ForeignKey(IncomeTaxPolicy, on_delete=models.PROTECT)
    min_amount = models.IntegerField()
    max_amount = models.IntegerField()
    pctg_tax = models.FloatField()

class EmployeeSalary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.PROTECT)
    gross_salary = models.IntegerField(blank=True, null=True)
    hour_salary = models.IntegerField(blank=True, null=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class EmployeeWorkShift(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.PROTECT)
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    duration = models.FloatField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=WorkShiftStatus.choices(), max_length=50)

class PaymentPeriod(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class EmployeePrepaid(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.PROTECT)
    period = models.ForeignKey(PaymentPeriod, on_delete=models.PROTECT)
    amount = models.IntegerField()

    create_date = models.DateTimeField(auto_now_add=True)
    approve_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(auto_now=True)

    ledger = models.OneToOneField('accounting.Ledger', 
        related_name='ledger_employee_prepaid',
        on_delete=models.CASCADE
    )

    status = models.CharField(choices=PrepaidStatus.choices(), 
                        default=PrepaidStatus.DRAFT.name,
                        max_length=50)

class Payroll(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    period = models.ForeignKey(PaymentPeriod, on_delete=models.PROTECT)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)

    create_date = models.DateTimeField(auto_now_add=True)
    approve_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(auto_now=True)

    ledger = models.OneToOneField('accounting.Ledger', 
        related_name='ledger_payroll',
        on_delete=models.CASCADE
    )

    status = models.CharField(choices=PayrollStatus.choices(), 
                    default=PayrollStatus.DRAFT.name,
                    max_length=50)

class EmployeePayment(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.PROTECT)
    payroll = models.ForeignKey(Payroll, on_delete=models.PROTECT)

    amount_gross = models.IntegerField()
    amount_bonus = models.IntegerField()
    amount_tax = models.IntegerField()
    amount_prepaid = models.IntegerField()
    amount_net = models.IntegerField()

    ledger_item = models.OneToOneField('accounting.LedgerItem',
        related_name='ledger_employee_payment',
        on_delete=models.PROTECT
    )