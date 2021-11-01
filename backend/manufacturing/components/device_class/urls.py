from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', DeviceClassTableView.as_view()),
    path('search-category', CategoryAsyncSearchView.as_view()),
    path('change-status/<pk>', change_device_class_status),
]

router = DefaultRouter()
router.register('crud', DeviceClassViewSet)
urlpatterns += router.urls
