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
            'name': 'note',
            'title': 'Diễn giải',
            'width': '45%',
        },
        {
            'name': 'date',
            'title': 'Ngày chuyển',
            'width': '20%'
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

    def get_queryset(self, user):
        return Exchange.objects.filter(company=user.employee.company)
