from django.contrib import admin

from .models import *

admin.site.register(Account)
admin.site.register(AccountBalanceHistory)
admin.site.register(Bank)
admin.site.register(BankAccount)

admin.site.register(Invoice)
admin.site.register(Ledger)
admin.site.register(LedgerItem)

admin.site.register(ExpenseType)
admin.site.register(Expense)
admin.site.register(ExpenseItem)

admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(IncomeItem)

admin.site.register(InternalTransfer)
admin.site.register(InternalTransferItem)