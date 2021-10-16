import json
from django.shortcuts import get_object_or_404, render

from .forms import *
from .serializers import OrderLineSerializer

# Create your views here.

def list_order(request):
    return render(request, 'purchase/order/list.html')

def create_order(request):
    company = request.user.staff.company
    form = OrderForm(company=company)
    context = {
        'form': form,
        'order_lines_json': '[]',
    }
    return render(request, 'purchase/order/form.html', context)

def get_order_lines_json(order):
    order_lines = order.order_lines.all()
    data = OrderLineSerializer(order_lines, many=True).data
    return json.dumps(data)

def update_order(request, pk):
    company = request.user.staff.company
    instance = get_object_or_404(Order, pk=pk, company=company)
    form = OrderForm(company=company, instance=instance)
    context = {
        'form': form,
        'order_lines_json': get_order_lines_json(instance)
    }
    return render(request, 'purchase/order/form.html', context)
