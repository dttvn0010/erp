from django.urls import path
from rest_framework.routers import DefaultRouter
from .views_api import *

urlpatterns = [
    path('change-status/<pk>', change_product_status),
]

router = DefaultRouter()
router.register('crud', ProductViewSet)
urlpatterns += router.urls
