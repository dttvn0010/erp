from django.urls import path, include

urlpatterns = [
    path('account/', include('accounting.components.account.urls')),
    path('bank/', include('accounting.components.bank.urls')),
    path('bank-account/', include('accounting.components.bank_account.urls')),
    path('expense-type/', include('accounting.components.expense_type.urls')),
    path('income-type/', include('accounting.components.income_type.urls')),
]