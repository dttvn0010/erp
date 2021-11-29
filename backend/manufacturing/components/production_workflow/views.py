from core.utils.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, DataAsyncSearchView, ChangeItemStatusView
from manufacturing.models import ProductBom, WorkCenter, DeviceClass
from .serializers import *

class ProductionWorkflowTableView(DataTableView):
    model = ProductionWorkflow
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '32%'
        },
        {
            'name': 'bom',
            'display_field': 'name',
            'title': 'Định lượng NVL',
            'search_options': {
                'async': True,
                'company_field': 'product.company'
            },
            'width': '32%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
            'width': '32%'
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
        return ProductionWorkflow.objects.filter(bom__product__company=user.employee.company)

class ProductionWorkflowViewSet(ModelViewSet):
    queryset = ProductionWorkflow.objects.all()
    serializer_class = ProductionWorkflowSerializer

class ChangeProductionWorkflowStatusView(ChangeItemStatusView):
    model = ProductionWorkflow
    company_field = 'bom.product.company'

class ProductBomAsyncSearchView(DataAsyncSearchView):
    fields = ['name']
    company_field = 'product.company'
    model = ProductBom

class WorkCenterAsyncSearchView(DataAsyncSearchView):
    model = WorkCenter
    fields = ['name']

class DeviceClassAsyncSearchView(DataAsyncSearchView):
    model = DeviceClass
    fields = ['name']