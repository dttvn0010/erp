from django.urls import path
from .views import *

urlpatterns = [
    path('', list_product),
    path('create', create_product),
    path('update/<pk>', update_product),
    path('delete/<pk>', delete_product),
    path('search', ProductTableView.as_view()),
    path('search-category', ProductCategoryAsyncSearchView.as_view()),
]