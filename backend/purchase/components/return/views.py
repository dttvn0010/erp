from core.views_api import DataTableView
from purchase.models import Order
from core.constants import BaseStatus

class ReturnTableView(DataTableView):
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
            'display_list': BaseStatus.choices(),
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

    def get_queryset(self, user):
        return Order.objects.none()