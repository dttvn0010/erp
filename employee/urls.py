from django.urls import path
from .views import *

urlpatterns = [
    path('user', list_user),
    path('group', list_group),
    path('department', list_department),
    path('team', list_team),
]