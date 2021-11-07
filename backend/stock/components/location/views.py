from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, ChangeItemStatusView
from core.constants import BaseStatus
from .serializers import *

class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class LocationTableView(DataTableView):
    model = Location
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '30%'
        },
        {
            'name': 'address',
            'title': 'Địa chỉ',
            'width': '35%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'edit_list': BaseStatus.choices(excludes=[BaseStatus.DRAFT.name]),
            'title': 'Trạng thái',
            'orderable': False,
            'editable': True,
            'width': '30%'
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
        return Location.objects.filter(company=user.employee.company)

class ChangeLocationStatusView(ChangeItemStatusView):
    model = Location