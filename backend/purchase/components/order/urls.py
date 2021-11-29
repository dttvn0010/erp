from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    path('search', OrderTableView.as_view()),
]

router = DefaultRouter()
router.register('crud', OrderViewSet)
urlpatterns += router.urls
