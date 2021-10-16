from django.urls import path
from .views import *

urlpatterns = [
    path('search', VoucherTableView.as_view()),
]