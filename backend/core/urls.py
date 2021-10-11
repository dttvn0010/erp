from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('app', app),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('partner/', include('core.components.partner.urls')),
    path('api/', include('core.urls_api')),
]