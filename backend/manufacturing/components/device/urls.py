from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', DeviceTableView.as_view()),
    path('search-device-class', DeviceClassAsyncSearchView.as_view()),
    path('change-status/<pk>', change_device_status),
]

router = DefaultRouter()
router.register('crud', DeviceViewSet)
urlpatterns += router.urls
