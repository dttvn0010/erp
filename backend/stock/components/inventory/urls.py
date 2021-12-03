from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', InventoryTableView.as_view()),
]

router = DefaultRouter()
router.register('crud', InventoryViewSet)
urlpatterns += router.urls
