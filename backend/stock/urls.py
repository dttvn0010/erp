from django.urls import path, include
from .views import *

urlpatterns = [
    path('search-product', ProductAsyncSearchView.as_view()),
    path('search-location', LocationAsyncSearchView.as_view()),

    path('location/', include('stock.components.location.urls')),
    path('product-category/', include('stock.components.product_category.urls')),
    path('product/', include('stock.components.product.urls')),
    path('product-quantity/', include('stock.components.product_quantity.urls')),
    path('import/', include('stock.components.import.urls')),
    path('export/', include('stock.components.export.urls')),
    path('exchange/', include('stock.components.exchange.urls')),
    path('inventory/', include('stock.components.inventory.urls')),
]