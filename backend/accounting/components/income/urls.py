from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', IncomeTableView.as_view()),
    path('search-income-type', IncomeTypeAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', IncomeViewSet)
urlpatterns += router.urls
