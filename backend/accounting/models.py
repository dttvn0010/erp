from django.db import models
from core.models import Partner
from core.models import User, Company
from core.constants import BaseStatus
from .constants import ExpenseStatus, BusinessType, BankAccountType

# Create your models here.
class Account(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    code = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('Account', blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200, blank=True)
    balance = models.IntegerField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class AccountBalanceHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT) 
    balance = models.IntegerField()
    
    ref_ledger_item = models.ForeignKey('LedgerItem', 
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    date = models.DateTimeField()

class Bank(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='static/images/bank-logos')

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    bank_branch = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=50)
    account_holder = models.CharField(max_length=200)

    type = models.CharField(choices=BankAccountType.choices(), max_length=50)
    ref_pk = models.BigIntegerField(blank=True, null=True)
    ref_class = models.CharField(blank=True, max_length=200)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)
    
    def __str__(self):
        return self.name

class IncomeType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class ExpenseType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT)
    partner_tax_number = models.CharField(max_length=50, blank=True)
    partner_name = models.CharField(max_length=200)
    partner_address = models.CharField(max_length=300, blank=True)
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateTimeField()
    
class Ledger(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    business_type = models.CharField(choices=BusinessType.choices(), max_length=50)

    inward = models.BooleanField(null=True)
    internal = models.BooleanField(default=False)
    cash = models.BooleanField(default=True)

    from_bank_account = models.ForeignKey(BankAccount, 
        related_name='ledger_from_bank_accounts',
        blank=True, null=True, 
        on_delete=models.PROTECT
    )

    to_bank_account = models.ForeignKey(BankAccount, 
        related_name='ledger_to_bank_accounts',
        blank=True, null=True, 
        on_delete=models.PROTECT
    )
    
    memo = models.CharField(max_length=200, blank=True)
    amount = models.IntegerField()

    ref_pk = models.BigIntegerField(null=True)
    ref_class = models.CharField(blank=True, max_length=200)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.memo

class LedgerItem(models.Model):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    
    debit_account = models.ForeignKey(Account, 
        related_name='ledger_debit_accounts',
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    credit_account = models.ForeignKey(Account, 
        related_name='ledger_credit_accounts',
        blank=True, null=True,
        on_delete=models.PROTECT
    )
    
    note = models.CharField(max_length=200, blank=True)
    amount = models.IntegerField()
    
    ref_pk = models.BigIntegerField(blank=True, null=True)
    ref_class = models.CharField(max_length=200, blank=True)

class InternalTransfer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    
    ledger = models.OneToOneField(Ledger,
        related_name='ledger_internal_transfer',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self) -> str:
        return self.ledger.memo

class InternalTransferItem(models.Model):
    transfer = models.ForeignKey(InternalTransfer, related_name='items', on_delete=models.PROTECT)

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_internal_transfer_item',
        on_delete=models.PROTECT
    )

class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    ledger = models.OneToOneField(Ledger, 
        related_name='ledger_expense',
        on_delete=models.CASCADE
    )

    request_date = models.DateTimeField(blank=True, null=True)
    approve_date = models.DateTimeField(blank=True, null=True)

    request_person = models.ForeignKey(User, related_name='request_expenses', 
            blank=True, null=True,
            on_delete=models.PROTECT)

    approve_person = models.ForeignKey(User, related_name='approve_expenses', 
            blank=True, null=True,
            on_delete=models.PROTECT)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=ExpenseStatus.choices(), 
            default=ExpenseStatus.DRAFT.name, max_length=50)

    def __str__(self) -> str:
        return self.ledger.memo

class ExpenseItem(models.Model):
    expense = models.ForeignKey(Expense, related_name='items', on_delete=models.CASCADE)

    type = models.ForeignKey(ExpenseType, 
        blank=True, null=True, 
        on_delete=models.PROTECT
    )

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_expense_item',
        on_delete=models.PROTECT
    )

class Income(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    ledger = models.OneToOneField(Ledger, 
        related_name='ledger_income',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self) -> str:
        return self.ledger.memo

class IncomeItem(models.Model):
    income = models.ForeignKey(Income, related_name='items', on_delete=models.CASCADE)

    type = models.ForeignKey(IncomeType, 
        blank=True, null=True, 
        on_delete=models.PROTECT
    )
    
    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_income_item',
        on_delete=models.PROTECT
    )