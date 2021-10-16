from django.urls import path
from .views import *

urlpatterns = [
    path('search', ReturnTableView.as_view()),
]