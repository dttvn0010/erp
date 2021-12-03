from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', DepartmentTableView.as_view()),
    path('change-status/<pk>', ChangeDepartmentStatusView.as_view()),
    path('search-parent', ParentAsyncSearchView.as_view()),
    path('search-employee', EmployeeAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', DepartmentViewSet)
urlpatterns += router.urls
