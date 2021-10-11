from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', list_location),
    path('search', LocationTableView.as_view()),
    path('change-status/<pk>', change_location_status),
]

router = DefaultRouter()
router.register('crud', LocationViewSet)
urlpatterns += router.urls
