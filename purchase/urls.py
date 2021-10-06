from django.urls import path, include

urlpatterns = [
    path('order/', include('purchase.components.order.urls')),
]