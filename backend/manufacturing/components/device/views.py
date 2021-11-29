from core.constants import BaseStatus
from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, DataAsyncSearchView, ChangeItemStatusView
from manufacturing.models import DeviceClass, WorkCenter

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

    def get_queryset(self, user, params):
        return Device.objects.filter(company=user.employee.company)

class DeviceClassAsyncSearchView(DataAsyncSearchView):
    model = DeviceClass
    fields = ['name']
    
class WorkCenterAsyncSearchView(DataAsyncSearchView):
    model = WorkCenter
    fields = ['name']

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class ChangeDeviceStatusView(ChangeItemStatusView):
    model = Device