from django.urls import path, include
from .views import *

urlpatterns = [
    path('order', list_order),

    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-customer', CustomerAsyncSearchView.as_view()),
    path('search-staff', StaffAsyncSearchView.as_view()),

    path('voucher/', include('sales.components.voucher.urls')),
    path('discount/', include('sales.components.discount.urls')),
    path('return/', include('sales.components.return.urls')),
]