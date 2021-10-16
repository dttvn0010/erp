from django.urls import path
from .views import *

urlpatterns = [
    path('search', DiscountTableView.as_view()),
]