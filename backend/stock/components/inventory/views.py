from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView
from core.constants import BaseStatus
from .serializers import *

class InventoryViewSet(ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

class InventoryTableView(DataTableView):
    model = Inventory
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'inventory_number',
            'title': 'Số đợt kiểm kê',
            'width': '20%'
        },
        {
            'name': 'location',
            'title': 'Địa điểm kho',
            'display_field': 'name',
            'width': '25%'
        },
        {
            'name': 'date',
            'title': 'Ngày kiểm kê',
            'format': '%d/%m/%Y %H:%M',
            'width': '20%'
        },
        {
            'name': 'note',
            'title': 'Ghi chú',
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
        return Inventory.objects.filter(location__company=user.employee.company)