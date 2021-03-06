from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, ChangeItemStatusView
from core.constants import BaseStatus
from .serializers import *

class ExpenseTypeViewSet(ModelViewSet):
    serializer_class = ExpenseTypeSerializer
    queryset = ExpenseType.objects.all()

class ExpenseTypeTableView(DataTableView):
    model = ExpenseType
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '30%'
        },
        {
            'name': 'description',
            'title': 'Mô tả',
            'width': '35%'
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
        return ExpenseType.objects.filter(company=user.employee.company)

class ChangeExpenseTypeStatusView(ChangeItemStatusView):
    model = ExpenseType