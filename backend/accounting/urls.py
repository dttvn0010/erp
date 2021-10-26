from django.urls import path, include

from .views import *

urlpatterns = [
    path('search-account', AccountAsyncSearchView.as_view()),
    path('search-bank-account', BankAccountAsyncSearchView.as_view()),

    path('account/', include('accounting.components.account.urls')),
    path('bank/', include('accounting.components.bank.urls')),
    path('bank-account/', include('accounting.components.bank_account.urls')),
    path('expense-type/', include('accounting.components.expense_type.urls')),
    path('expense/', include('accounting.components.expense.urls')),
    path('income-type/', include('accounting.components.income_type.urls')),
    path('income/', include('accounting.components.income.urls')),
    path('internal-transfer/', include('accounting.components.internal_transfer.urls')),
]