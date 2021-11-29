from core.utils.viewsets import ModelViewSet
from stock.models import Import
from core.views_api import DataTableView
from .serializers import *

class ImportViewSet(ModelViewSet):
    serializer_class = ImportSerializer
    queryset = Import.objects.all()

class ImportDataTableView(DataTableView):
    model = Import
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'note',
            'title': 'Diễn giải',
            'width': '45%',
        },
        {
            'name': 'date',
            'title': 'Ngày nhập',
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

    def get_queryset(self, user, params):
        return Import.objects.filter(company=user.employee.company)
