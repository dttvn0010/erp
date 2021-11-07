from django.urls import path
from rest_framework.routers import DefaultRouter
from .views_api import *

urlpatterns = [
    path('change-status/<pk>', ChangeProductCategoryStatusView.as_view()),
]

router = DefaultRouter()
router.register('crud', ProductCategoryViewSet)
urlpatterns += router.urls
