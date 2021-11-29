from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, DataAsyncSearchView
from core.utils.date_utils import format_datetime 
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

    def get_queryset(self, user, params):
        return DeviceMaintainance.objects.filter(device__company=user.employee.company)

    def get_start_date(self, obj, context):
        return format_datetime(obj.start_date or obj.planned_start_date)

    def get_end_date(self, obj, context):
        return format_datetime(obj.end_date or obj.planned_end_date)

class DeviceAsyncSearchView(DataAsyncSearchView):
    model = Device
    fields = ['name']

class DeviceMaintainanceViewSet(ModelViewSet):
    queryset = DeviceMaintainance.objects.all()
    serializer_class = DeviceMaintainanceSerializer