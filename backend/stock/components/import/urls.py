from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns =[
    path('search', ImportDataTableView.as_view()),
]

router = DefaultRouter()
router.register('crud', ImportViewSet)
urlpatterns += router.urls
