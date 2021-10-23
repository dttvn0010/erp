from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ExpenseTypeTableView.as_view()),
    path('change-status/<pk>', change_expense_type_status),
]

router = DefaultRouter()
router.register('crud', ExpenseTypeViewSet)
urlpatterns += router.urls
