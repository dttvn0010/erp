from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', BankAccountTableView.as_view()),
    path('change-status/<pk>', ChangeBankAccountStatusView.as_view()),
    path('search-bank', BankAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', BankAccountViewSet)
urlpatterns += router.urls
