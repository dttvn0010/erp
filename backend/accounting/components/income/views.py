from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, DataAsyncSearchView
from core.constants import BaseStatus
from accounting.models import IncomeType
from .serializers import *

class IncomeViewSet(ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

class IncomeTableView(DataTableView):
    model = Income
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'amount',
            'source': 'ledger.amount',
            'title': 'Số tiền',
            'width': '15%'
        },
        {
            'name': 'payment_type',
            'source': 'ledger.cash',
            'display_list': [
                (True, 'Tiền mặt'),
                (False, 'Chuyển khoản')
            ],
            'title': 'Hình thức thanh toán',
            'width': '15%'
        },
        {
            'name': 'note',
            'source': 'ledger.memo',
            'title': 'Ghi chú',
            'width': '25%'
        },
        {
            'name': 'date',
            'format': '%d/%m/%Y %H:%M',
            'title': 'Ngày thu',
            'width': '15%'
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

    def filter_by_payment_type(self, queryset, value):
        value = map(lambda x: x == 'true', value.split(','))
        return queryset.filter(ledger__cash__in=value)

    def get_queryset(self, user, params):
        return Income.objects.filter(company=user.employee.company)

class IncomeTypeAsyncSearchView(DataAsyncSearchView):
    model = IncomeType
    fields = ['name']