
from core.views_api import AsyncSearchView
from core.models import Partner
from employee.models import Employee
from stock.models import Product

from core.constants import BaseStatus

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
            is_supplier=True,
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