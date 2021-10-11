from django.urls import path, include

urlpatterns = [
    path('location/', include('stock.components.location.urls')),
    path('product-category/', include('stock.components.product_category.urls')),
    path('product/', include('stock.components.product.urls')),
]