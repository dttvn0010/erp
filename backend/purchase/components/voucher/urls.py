from django.urls import path, include
from .views import *
from .views_api import ProductAsyncSearchView, StaffAsyncSearchView, SuppilerAsyncSearchView, VoucherTableView, delete_order

urlpatterns = [
    path('', list_order),
    path('search', VoucherTableView.as_view()),
    path('create', create_order),
    path('update/<pk>', update_order),
    path('delete/<pk>', delete_order),
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-supplier', SuppilerAsyncSearchView.as_view()),
    path('search-staff', StaffAsyncSearchView.as_view()),
    path('api/', include('purchase.components.voucher.urls_api'))
]