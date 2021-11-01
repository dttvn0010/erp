from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, AsyncSearchView
from manufacturing.models import DeviceCategory
from .serializers import *

class DeviceClassTableView(DataTableView):
    model = DeviceClass
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'category',
            'display_field': 'name',
            'title': 'Nhóm',
            'width': '25%',
        },
        {
            'name': 'code',
            'title': 'Mã',
            'width': '20%'
        },
        {
            'name': 'name',
            'title': 'Tên',
            'width': '25%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
            'width': '25%'
        },
        {
            'title': 'Thao tác',
            'orderable': False,
            'search': False,
            'css_class': 'text-center',
            'width': '5%'
        },
    ]

    def get_queryset(self, user):
        return DeviceClass.objects.filter(company=user.employee.company)

class CategoryAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return DeviceCategory.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class DeviceClassViewSet(ModelViewSet):
    queryset = DeviceClass.objects.all()
    serializer_class = DeviceClassSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

@api_view(['POST'])
def change_device_class_status(request, pk):
    device_class = get_object_or_404(DeviceClass, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if device_class.status != BaseStatus.ACTIVE.name:
        device_class.status = BaseStatus.ACTIVE.name
    else:
        device_class.status = BaseStatus.INACTIVE.name

    device_class.save()
    return Response({'success': True})