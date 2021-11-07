from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', LocationTableView.as_view()),
    path('change-status/<pk>', ChangeLocationStatusView.as_view()),
]

router = DefaultRouter()
router.register('crud', LocationViewSet)
urlpatterns += router.urls
