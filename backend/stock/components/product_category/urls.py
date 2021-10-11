from django.urls import path, include
from .views import *

urlpatterns = [
    path('', list_product_category),
    path('create', create_product_category),
    path('update/<pk>', update_product_category),
    path('delete/<pk>', delete_product_category),
    path('search', ProductCategoryTableView.as_view()),
    path('search-parent', ParentAsyncSearchView.as_view()),
    path('api/', include('stock.components.product_category.urls_api'))
]