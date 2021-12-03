from core.utils.viewsets import ModelViewSet
from stock.models import Exchange
from core.views_api import DataTableView
from .serializers import *

class ExchangeViewSet(ModelViewSet):
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()

class ExchangeDataTableView(DataTableView):
    model = Exchange
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'exchange_number',
            'title': 'Số phiếu chuyển kho',
            'width': '30%',
        },
        {
            'name': 'date',
            'title': 'Ngày chuyển',
            'width': '20%'
        },
        {
            'name': 'note',
            'title': 'Ghi chú',
            'width': '45%',
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
        return Exchange.objects.filter(company=user.employee.company)