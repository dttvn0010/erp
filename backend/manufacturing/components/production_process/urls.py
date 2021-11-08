from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ProductionProcessTableView.as_view()),
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-product-bom', ProductBomAsyncSearchView.as_view()),
    path('search-production-workflow', ProductionWorkflowAsyncSearchView.as_view()),
    path('search-device-class', DeviceClassAsyncSearchView.as_view()),
    path('search-device', DeviceAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', ProductionProcessViewSet)
urlpatterns += router.urls
