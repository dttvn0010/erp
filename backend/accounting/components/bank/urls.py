from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', BankTableView.as_view()),
    path('change-status/<pk>', ChangeBankStatusView.as_view()),
]

router = DefaultRouter()
router.register('crud', BankViewSet)
urlpatterns += router.urls
