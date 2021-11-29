from django.urls import path, include
from .views import *

urlpatterns = [
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-stock-location', StockLocationAsyncSearchView.as_view()),
    path('search-expense-type', ExpenseTypeAsyncSearchView.as_view()),
    path('search-customer', CustomerAsyncSearchView.as_view()),
    path('search-employee', EmployeeAsyncSearchView.as_view()),
    path('search-bank-account', BankAccountAsyncSearchView.as_view()),
    path('order/', include('sales.components.order.urls')),
]