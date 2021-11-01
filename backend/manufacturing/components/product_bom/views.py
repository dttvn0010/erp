from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, AsyncSearchView
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

class ProductAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return Product.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class ProductBomViewSet(ModelViewSet):
    queryset = ProductBom.objects.all()
    serializer_class = ProductBomSerializer

@api_view(['POST'])
def change_product_bom_status(request, pk):
    bom = get_object_or_404(ProductBom, 
        pk=pk,
        product__company=request.user.employee.company
    )
    
    if bom.status != BaseStatus.ACTIVE.name:
        bom.status = BaseStatus.ACTIVE.name
    else:
        bom.status = BaseStatus.INACTIVE.name

    bom.save()
    return Response({'success': True})