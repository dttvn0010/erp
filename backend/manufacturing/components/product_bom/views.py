from core.utils.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, DataAsyncSearchView, ChangeItemStatusView
from stock.models import Product

from .serializers import *

class ProductBomTableView(DataTableView):
    model = ProductBom
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '35%'
        },

        {
            'name': 'product',
            'display_field': 'name',
            'title': 'Thành phẩm',
            'width': '30%',
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
        return ProductBom.objects.filter(product__company=user.employee.company)

class ProductAsyncSearchView(DataAsyncSearchView):
    model = Product
    fields = ['name']

class ProductBomViewSet(ModelViewSet):
    queryset = ProductBom.objects.all()
    serializer_class = ProductBomSerializer

class ChangeProductBomStatusView(ChangeItemStatusView):
    model = ProductBom