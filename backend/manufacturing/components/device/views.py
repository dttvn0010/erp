from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, AsyncSearchView
from manufacturing.models import DeviceClass

from .serializers import *

class DeviceTableView(DataTableView):
    model = Device
    order_by = '-update_date'
    columns_def = [
        {
            'name': '_class',
            'display_field': 'name',
            'title': 'Thiết bị OEM',
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
        return Device.objects.filter(company=user.employee.company)

class DeviceClassAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return DeviceClass.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

@api_view(['POST'])
def change_device_status(request, pk):
    device = get_object_or_404(Device, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if device.status != BaseStatus.ACTIVE.name:
        device.status = BaseStatus.ACTIVE.name
    else:
        device.status = BaseStatus.INACTIVE.name

    device.save()
    return Response({'success': True})