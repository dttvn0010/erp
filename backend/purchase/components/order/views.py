
from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView
from purchase.models import Order

from purchase.constants import OrderStatus
from .serializers import *

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderTableView(DataTableView):
    model = Order
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'order_number',
            'title': 'Số đơn hàng',
            'width': '24%',
        },
        {
            'name': 'supplier',
            'display_field': 'name',
            'title': 'Nhà cung cấp',
            'width': '24%'
        },
        {
            'name': 'note',
            'title': 'Ghi chú',
            'orderable': False,
            'width': '24%'
        },
        {
            'name': 'status',
            'display_list': OrderStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
            'width': '24%'
        },
        {
            'title': 'Thao tác',
            'orderable': False,
            'search': False,
            'css_class': 'text-center',
            'width': '4%'
        },
    ]

    def get_queryset(self, user, params):
        type_ = params.get('type', '')
        return Order.objects.filter(company=user.employee.company, type=type_.upper())