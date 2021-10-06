from django.db import models
from django.utils.translation import gettext as _
from core.models import User, Company
from core.constants import BaseStatus
from .constants import ExpenseStatus, InvoiceType

# Create your models here.
class Bank(models.Model):
    swift_code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    account_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    invoice_type = models.CharField(choices=InvoiceType.choices(), max_length=50)
    incoming = models.BooleanField()
    note = models.CharField(max_length=500)
    bank_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.PROTECT)
    amount_untaxed = models.IntegerField()
    amount_tax = models.IntegerField()
    amount_total = models.IntegerField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    date = models.DateTimeField()

class ExpenseType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    code = models.CharField(max_length=100, 
                verbose_name=_("verbose_name.category.code"))

    name = models.CharField(max_length=200, 
                verbose_name=_("verbose_name.category.name"))

    description = models.CharField(max_length=500, 
                verbose_name=_("verbose_name.category.description"))

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    expense_type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT)

    amount = models.IntegerField()

    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)

    request_person = models.ForeignKey(User, related_name='request_expenses', 
            on_delete=models.PROTECT)

    approve_person = models.ForeignKey(User, related_name='approve_expenses', 
            on_delete=models.PROTECT)

    note = models.CharField(max_length=500)

    request_date = models.DateTimeField(null=True)
    approve_date = models.DateTimeField(null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=ExpenseStatus.choices(), max_length=50)