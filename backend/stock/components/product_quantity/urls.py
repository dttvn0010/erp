from django.urls import path
from .views import *

urlpatterns = [
    path('search', ProductQuantityTableView.as_view()),
    path('history', ProductQuantityHistoryTableView.as_view()),
    path('get-info/<pk>', get_product_quantity_info),
]