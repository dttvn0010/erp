from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import *

urlpatterns = [
    path('detail/<pk>', get_order_detail),
    path('save', save_order),
    path('delete/<pk>', delete_order),
    path('change-status/<pk>', change_order_status),
]

router = DefaultRouter()
router.register('crud', OrderViewSet)
urlpatterns += router.urls