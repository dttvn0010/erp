from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', DeviceMaintainanceTableView.as_view()),
    path('search-device', DeviceAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', DeviceMaintainanceViewSet)
urlpatterns += router.urls
