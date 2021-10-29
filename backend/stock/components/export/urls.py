from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns =[   
]

router = DefaultRouter()
router.register('crud', ExportViewSet)
urlpatterns += router.urls
