from core.utils.viewsets import ModelViewSet
from stock.models import Export
from core.views_api import DataTableView
from .serializers import *

class ExportViewSet(ModelViewSet):
    serializer_class = ExportSerializer
    queryset = Export.objects.all()

class ExportDataTableView(DataTableView):
    model = Export
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'export_number',
            'title': 'Số phiếu xuất',
            'width': '30%',
        },
        {
            'name': 'date',
            'title': 'Ngày xuất',
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
        return Export.objects.filter(company=user.employee.company)