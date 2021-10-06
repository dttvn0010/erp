from django.shortcuts import render

# Create your views here.
def list_order(request):
    return render(request, 'sales/order/list.html')