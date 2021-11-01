from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView, AsyncSearchView
from core.utils.date_utils import formatDateTime 
from core.constants import BaseStatus
from manufacturing.constants import DeviceMaintainanceStatus
from manufacturing.models import Device
from .serializers import *

class DeviceMaintainanceTableView(DataTableView):
    model = DeviceMaintainance
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'device',
            'display_field': 'name',
            'title': 'Thiết bị',
            'width': '25%',
        },
        {
            'name': 'start_date',
            'title': 'Thời gian bắt đầu',
            'width': '23%'
        },
        {
            'name': 'end_date',
            'title': 'Thời gian kết thúc',
            'width': '23%'
        },
        {
            'name': 'status',
            'display_list': DeviceMaintainanceStatus.choices(),
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
        return DeviceMaintainance.objects.filter(device__company=user.employee.company)

    def get_start_date(self, obj, context):
        return formatDateTime(obj.start_date or obj.planned_start_date)

    def get_end_date(self, obj, context):
        return formatDateTime(obj.end_date or obj.planned_end_date)

class DeviceAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return Device.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class DeviceMaintainanceViewSet(ModelViewSet):
    queryset = DeviceMaintainance.objects.all()
    serializer_class = DeviceMaintainanceSerializer