from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', EmployeeTableView.as_view()),
    path('search-department', DepartmentAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', EmployeeViewSet)
urlpatterns += router.urls
