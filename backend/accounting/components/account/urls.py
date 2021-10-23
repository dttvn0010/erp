from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', AccountTableView.as_view())
]

router = DefaultRouter()
router.register('crud', AccountViewSet)
urlpatterns += router.urls
