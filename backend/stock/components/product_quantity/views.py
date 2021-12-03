from rest_framework.response import Response
from rest_framework.decorators import api_view

from stock.models import ProductQuantity
from core.views_api import DataTableView
from core.constants import BaseStatus
from core.utils.date_utils import format_date

@api_view(['GET'])
def get_product_quantity_info(request, pk):
    product_quantity = ProductQuantity.objects.get(pk=pk)
    return Response({
        'location': {
            'id': product_quantity.location.id,
            'name': product_quantity.location.name,
        },
        'product': {
            'id': product_quantity.product.id,
            'name': product_quantity.product.name,
        }
    })

class ProductQuantityTableView(DataTableView):
    model = ProductQuantity
    order_by = '-create_date'
    columns_def = [
        {
            'name': 'location',
            'display_field': 'name',
            'title': 'Kho',
            'width': '35%'
        },
        {
            'name': 'product',
            'display_field': 'name',
            'title': 'Sản phẩm',
            'width': '35%'
        },
        {
            'name': 'qty',
            'title': 'Số lượng',
            'width': '25%'
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
        return ProductQuantity.objects.filter(
                product__company=user.employee.company,
                is_latest=True
            )

class ProductQuantityHistoryTableView(DataTableView):
    model = ProductQuantity
    order_by = '-create_date'

    columns_def = [
        {
            'name': 'create_date',
            'title': 'Ngày cập nhật',
            'width': '25%'
        },
        {
            'name': 'qty',
            'title': 'Số lượng trong kho',
            'orderable': False,
            'search': False,
            'width': '25%'
        },
        {
            'name': 'note',
            'title': 'Ghi chú',
            'orderable': False,
            'search': False,
            'width': '50%'
        }
    ]

    def get_note(self, obj, context):
        if obj.ref_product_move:
            if obj.ref_product_move.inward:
                if not obj.ref_product_move.internal:
                    return f'Nhập vào {obj.ref_product_move.qty} đơn vị'
                else:
                    return f'Chuyển từ kho {ref_product_move.location} sang {obj.ref_product_move.qty} đơn vị'
            else:
                if not obj.ref_product_move.internal:
                    return f'Xuất ra {obj.ref_product_move.qty} đơn vị'
                else:
                    return f'Chuyển sang kho {ref_product_move.location_dest} sang {obj.ref_product_move.qty} đơn vị'
        
        elif obj.ref_inventory_item:
            return f'Kiểm kê ngày ' + format_date(obj.ref_inventory_item.inventory)

        return ''

    def get_queryset(self, user, params):
        location_id = params.get('location_id')
        product_id = params.get('product_id')

        return ProductQuantity.objects.filter(
                product__company=user.employee.company,
                location__id=location_id,
                product__id=product_id
            )