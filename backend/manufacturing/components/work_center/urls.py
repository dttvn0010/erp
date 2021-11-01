from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', WorkCenterTableView.as_view()),
    path('change-status/<pk>', change_work_center_status),
]

router = DefaultRouter()
router.register('crud', WorkCenterViewSet)
urlpatterns += router.urls
