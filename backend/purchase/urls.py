from django.urls import path, include

from .views import *

urlpatterns = [
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-supplier', SuppilerAsyncSearchView.as_view()),
    path('search-staff', StaffAsyncSearchView.as_view()),

    path('voucher/', include('purchase.components.voucher.urls')),
    path('discount/', include('purchase.components.discount.urls')),
    path('return/', include('purchase.components.return.urls')),
]