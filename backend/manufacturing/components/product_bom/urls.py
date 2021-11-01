from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('search', ProductBomTableView.as_view()),
    path('search-product', ProductAsyncSearchView.as_view()),
]

router = DefaultRouter()
router.register('crud', ProductBomViewSet)
urlpatterns += router.urls
