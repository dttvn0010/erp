from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ExpenseTypeTableView.as_view()),
    path('change-status/<pk>', ChangeExpenseTypeStatusView.as_view()),
]

router = DefaultRouter()
router.register('crud', ExpenseTypeViewSet)
urlpatterns += router.urls
