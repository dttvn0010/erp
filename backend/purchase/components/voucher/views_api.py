
import time
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from employee.models import Employee

from core.views_api import AsyncSearchView, DataTableView
from core.models import Partner
from employee.models import Employee
from stock.models import Product
from purchase.models import Order

from core.constants import BaseStatus
from .serializers import *

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class VoucherTableView(DataTableView):
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
        return Order.objects.filter(company=user.employee.company)

class ProductAsyncSearchView(AsyncSearchView):
    fields = ['name', 'price_unit']

    def get_price_unit(self, item):
        return item.list_price

    def get_queryset(self, term, request):
        company = request.user.employee.company

        return Product.objects.filter(
            company=company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class SuppilerAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        company = request.user.employee.company
        return Partner.objects.filter(
            company=company,
            user__display__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class EmployeeAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_name(self, item):
        return item.user.display

    def get_queryset(self, term, request):
        company = request.user.employee.company
        return Employee.objects.filter(
            company=company,
            user__display__icontains=term,
            user__is_active=True
        )

@api_view(['GET'])
def get_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, company=request.user.employee.company)
    data = OrderSerializer(order).data
    
    data['order_items'] = [
        OrderItemSerializer(item).data
        for item in order.order_items.all()
    ]

    return Response(data)

def validate_save_order(instance, data):
    errors = {}
    serializer = OrderSerializer(data=data, instance=instance)
    
    if not serializer.is_valid():
        errors = serializer.errors

    order_items = data.get('order_items', [])
    
    for i, order_item in enumerate(order_items):
        item_serializer = OrderItemSerializer(data=order_item)

        if not item_serializer.is_valid():
            errors[f'order_items[{i}]'] = item_serializer.errors
    
    return errors

def get_order_items(items_data):
    order_items = []

    for item_data in items_data:
        qty = int(item_data['qty'])
        price_unit = int(item_data['price_unit'])

        order_item = ProductMove()
        order_item.product = Product.objects.get(pk=item_data['product'])
        order_item.qty = qty
        order_item.price_unit = price_unit
        order_item.price_tax = 0
        order_item.discount = 0
        order_item.price_untaxed = order_item.price_total = qty * price_unit
        order_item.incomming = True
        order_items.append(order_item)

    return order_items

@api_view(['POST'])
def save_order(request):
    company =  request.user.employee.company
    data = request.data
    pk = data.get('id')
    instance = Order.objects.get(pk=pk) if pk else None

    errors = validate_save_order(instance, data)

    if len(errors) > 0:
        return Response(errors, status=400)

    if pk :
        order = get_object_or_404(Order, pk=pk, company=company)
        order.order_items.clear()
    else:
        order = Order()

    order.company =company
    order.order_number = str(int(time.time()))
    order.supplier = Partner.objects.get(pk=data['supplier'])
    order.note = data.get('note', '')
    order.save()
    
    order_items = get_order_items(data.get('order_items', []))

    for order_item in order_items:
        order_item.save()
        order.order_items.add(order_item)

    return Response({'success': True})

@api_view(['DELETE'])
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk, company=request.user.employee.company)
    order.delete()
    return Response({'success': True})

@api_view(['POST'])
def change_order_status(request, pk):
    order = get_object_or_404(Order, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if order.status != BaseStatus.ACTIVE.name:
        order.status = BaseStatus.ACTIVE.name
    else:
        order.status = BaseStatus.INACTIVE.name

    order.save()
    return Response({'success': True})