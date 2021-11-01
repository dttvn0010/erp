from django.urls import path, include

urlpatterns = [
    path('device/', include('manufacturing.components.device.urls')),
    path('device-category/', include('manufacturing.components.device_category.urls')),
    path('device-class/', include('manufacturing.components.device_class.urls')),
    path('device-maintainance/', include('manufacturing.components.device_maintainance.urls')),
    path('product-bom/', include('manufacturing.components.product_bom.urls')),
    path('production-workflow/', include('manufacturing.components.production_workflow.urls')),
    path('production-process/', include('manufacturing.components.production_process.urls')),
    path('work-center/', include('manufacturing.components.work_center.urls')),
]