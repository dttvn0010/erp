from django.urls import path, include
from .views import *

urlpatterns = [
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-stock-location', StockLocationAsyncSearchView.as_view()),
    path('search-expense-type', ExpenseTypeAsyncSearchView.as_view()),
    path('search-customer', CustomerAsyncSearchView.as_view()),
    path('search-employee', EmployeeAsyncSearchView.as_view()),

    path('voucher/', include('sales.components.voucher.urls')),
    path('discount/', include('sales.components.discount.urls')),
    path('return/', include('sales.components.return.urls')),
]