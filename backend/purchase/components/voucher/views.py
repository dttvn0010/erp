import json
from django.shortcuts import get_object_or_404, render

from .forms import *
from .serializers import OrderItemSerializer

# Create your views here.

def list_order(request):
    return render(request, 'purchase/order/list.html')

def create_order(request):
    company = request.user.employee.company
    form = OrderForm(company=company)
    context = {
        'form': form,
        'order_items_json': '[]',
    }
    return render(request, 'purchase/order/form.html', context)

def get_order_items_json(order):
    order_items = order.order_items.all()
    data = OrderItemSerializer(order_items, many=True).data
    return json.dumps(data)

def update_order(request, pk):
    company = request.user.employee.company
    instance = get_object_or_404(Order, pk=pk, company=company)
    form = OrderForm(company=company, instance=instance)
    context = {
        'form': form,
        'order_items_json': get_order_items_json(instance)
    }
    return render(request, 'purchase/order/form.html', context)
