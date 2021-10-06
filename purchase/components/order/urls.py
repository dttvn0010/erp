from django.urls import path
from .views import *
from .views_api import *

urlpatterns = [
    path('', list_order),
    path('search', OrderTableView.as_view()),
    path('create', create_order),
    path('update/<pk>', update_order),
    path('delete/<pk>', delete_order),
    path('save', save_order),
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-supplier', SuppilerAsyncSearchView.as_view()),
]