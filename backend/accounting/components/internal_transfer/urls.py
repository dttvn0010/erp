from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', InternalTransferTableView.as_view()),
]

router = DefaultRouter()
router.register('crud', InternalTransferViewSet)
urlpatterns += router.urls
