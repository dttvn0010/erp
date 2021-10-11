from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', PartnerTableView.as_view()),
    path('change-status/<pk>', change_partner_status),
]

router = DefaultRouter()
router.register('crud', PartnerViewSet)
urlpatterns += router.urls
