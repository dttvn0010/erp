from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', IncomeTypeTableView.as_view()),
    path('change-status/<pk>', ChangeIncomeTypeStatusView.as_view()),
]

router = DefaultRouter()
router.register('crud', IncomeTypeViewSet)
urlpatterns += router.urls
