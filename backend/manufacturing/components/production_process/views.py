from core.views_api import DataTableView, DataAsyncSearchView, AsyncSearchView
from core.constants import BaseStatus
from core.utils.viewsets import ModelViewSet
from core.utils.date_utils import format_datetime 

from manufacturing.models import(
    Product, 
    ProductBom, 
    ProductionWorkflow,
    DeviceClass,
    Device
)

from manufacturing.constants import ProductionProcessStatus

from .serializers import *

class ProductionProcessTableView(DataTableView):
    model = ProductionProcess
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'product',
            'source': 'bom.product',
            'display_field': 'name',
            'title': 'Thành phẩm',
            'search_options': {
                'async': True,
            },
            'width': '20%',
        },
        {
            'name': 'product_qty',
            'title': 'Số lượng',
            'width': '15%',
        },
        {
            'name': 'start_date',
            'title': 'Ngày bắt đầu',
            'width': '18%'
        },
        {
            'name': 'end_date',
            'title': 'Ngày kết thúc',
            'width': '18%'
        },
        {
            'name': 'status',
            'display_list': ProductionProcessStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
            'width': '25%'
        },
        {
            'title': 'Thao tác',
            'orderable': False,
            'search': False,
            'css_class': 'text-center',
            'width': '4%'
        },
    ]

    def get_start_date(self, obj, context):
        return format_datetime(obj.start_date or obj.planned_start_date)

    def get_end_date(self, obj, context):
        return format_datetime(obj.end_date or obj.planned_end_date)

    def get_queryset(self, user, params):
        return ProductionProcess.objects.filter(bom__product__company=user.employee.company)

class ProductionProcessViewSet(ModelViewSet):
    queryset = ProductionProcess.objects.all()
    serializer_class = ProductionProcessSerializer

class ProductAsyncSearchView(DataAsyncSearchView):
    fields = ['name']
    model = Product

class ProductBomAsyncSearchView(AsyncSearchView):
    fields = ['name']
    
    def get_queryset(self, term, request):
        
        product_id = request.GET.get('product_id')
        
        return ProductBom.objects.filter(
            product__id=product_id,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class ProductionWorkflowAsyncSearchView(AsyncSearchView):
    fields = ['name']
    
    def get_queryset(self, term, request):
        bom_id = request.GET.get('bom_id')

        queryset =  ProductionWorkflow.objects.filter(
            bom__id=bom_id,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

        return queryset

class DeviceClassAsyncSearchView(AsyncSearchView):
    fields = ['name']
    
    def get_queryset(self, term, request):
        workflow_step_id = request.GET.get('workflow_step_id')

        print('workflow_step_id=', workflow_step_id)
        
        return DeviceClass.objects.filter(
            productionworkflowstepdeviceuse__step__id=workflow_step_id,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class DeviceAsyncSearchView(AsyncSearchView):
    fields = ['name']
    
    def get_queryset(self, term, request):
        workflow_step_id = request.GET.get('workflow_step_id')
        device_class_id = request.GET.get('device_class_id')
        
        return Device.objects.filter(
            _class__id=device_class_id,
            workcenter__productionworkflowstep__id=workflow_step_id,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )