from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ProductionWorkflowTableView.as_view()),
    path('search-product-bom', ProductBomAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', ProductionWorkflowViewSet)
urlpatterns += router.urls
