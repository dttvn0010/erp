from core.utils.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, ChangeItemStatusView
from manufacturing.constants import WorkCenterState
from .serializers import *

class WorkCenterTableView(DataTableView):
    model = WorkCenter
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '35%'
        },
        {
            'name': 'working_state',
            'display_list': WorkCenterState.choices(),
            'title': 'Trạng thái hoạt động',
            'width': '30%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
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

    def get_queryset(self, user, params):
        return WorkCenter.objects.filter(company=user.employee.company)

class WorkCenterViewSet(ModelViewSet):
    queryset = WorkCenter.objects.all()
    serializer_class = WorkCenterSerializer

class ChangeWorkCenterStatusView(ChangeItemStatusView):
    model = WorkCenter