from core.utils.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, DataAsyncSearchView, ChangeItemStatusView
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

    def get_queryset(self, user, params):
        return DeviceClass.objects.filter(company=user.employee.company)

class CategoryAsyncSearchView(DataAsyncSearchView):
    model = DeviceCategory
    fields = ['name']

class DeviceClassViewSet(ModelViewSet):
    queryset = DeviceClass.objects.all()
    serializer_class = DeviceClassSerializer

class ChangeDeviceClassStatusView(ChangeItemStatusView):
    model = DeviceClass