from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ExpenseTableView.as_view()),
    path('search-expense-type', ExpenseTypeAsyncSearchView.as_view()),
    path('detail/<pk>', get_expense_detail),
    path('add-item/<pk>', add_expense_item),
    path('save', save_expense),
]

router = DefaultRouter()
router.register('crud', ExpenseViewSet)
urlpatterns += router.urls
