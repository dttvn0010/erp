from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ExpenseTableView.as_view()),
    path('search-expense-type', ExpenseTypeAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', ExpenseViewSet)
urlpatterns += router.urls
