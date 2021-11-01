from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', DeviceCategoryTableView.as_view()),
    path('search-parent', ParentAsyncSearchView.as_view()),
    path('change-status/<pk>', change_device_category_status),
]

router = DefaultRouter()
router.register('crud', DeviceCategoryViewSet)
urlpatterns += router.urls
