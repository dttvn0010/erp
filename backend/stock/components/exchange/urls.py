from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns =[   
    path('search', ExchangeDataTableView.as_view()),
]

router = DefaultRouter()
router.register('crud', ExchangeViewSet)
urlpatterns += router.urls
