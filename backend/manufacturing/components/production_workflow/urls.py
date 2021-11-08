from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ProductionWorkflowTableView.as_view()),
    path('search-product-bom', ProductBomAsyncSearchView.as_view()),
    path('search-work-center', WorkCenterAsyncSearchView.as_view()),
    path('search-device-class', DeviceClassAsyncSearchView.as_view()),
    path('change-status/<pk>', ChangeProductionWorkflowStatusView.as_view()),
]

router = DefaultRouter()
router.register('crud', ProductionWorkflowViewSet)
urlpatterns += router.urls
