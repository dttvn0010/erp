from django.shortcuts import render
from employee.models import Employee
from core.views_api import AsyncSearchView, DataAsyncSearchView
from core.models import Partner
from employee.models import Employee
from accounting.models import ExpenseType
from stock.models import Product, Location as StockLocation

from core.constants import BaseStatus

class ProductAsyncSearchView(DataAsyncSearchView):
    model = Product
    fields = ['name', 'price_unit']

    def get_price_unit(self, item):
        return item.list_price

class StockLocationAsyncSearchView(DataAsyncSearchView):
    model = StockLocation
    fields = ['name']

class CustomerAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        company = request.user.employee.company
        return Partner.objects.filter(
            company=company,
            is_customer=True,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )


class ExpenseTypeAsyncSearchView(DataAsyncSearchView):
    model = ExpenseType
    fields = ['name']

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