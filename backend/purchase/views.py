
from django.db.models import Q

from core.models import Partner
from employee.models import Employee
from accounting.models import ExpenseType, BankAccount
from stock.models import Product, Location as StockLocation
from core.views_api import AsyncSearchView, DataAsyncSearchView
from core.constants import BaseStatus
from accounting.constants import BankAccountType

class ProductAsyncSearchView(DataAsyncSearchView):
    model = Product
    fields = ['name', 'price_unit']

    def get_price_unit(self, item):
        return item.list_price

class StockLocationAsyncSearchView(DataAsyncSearchView):
    model = StockLocation
    fields = ['name']

class SuppilerAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        company = request.user.employee.company
        return Partner.objects.filter(
            company=company,
            is_supplier=True,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class EmployeeAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_name(self, item, context):
        return item.user.display

    def get_queryset(self, term, request):
        company = request.user.employee.company
        return Employee.objects.filter(
            company=company,
            user__display__icontains=term,
            user__is_active=True
        )

class ExpenseTypeAsyncSearchView(DataAsyncSearchView):
    model = ExpenseType
    fields = ['name']

class BankAccountAsyncSearchView(AsyncSearchView):
    fields = ['name', 'bank', 'account_number', 'account_holder']

    def get_queryset(self, term, request):
        supplier_id = request.GET.get('supplier_id')

        queryset =  BankAccount.objects.filter(
            Q(name__icontains=term) |
            Q(account_number__icontains=term) |
            Q(account_holder__icontains=term),
            company=request.user.employee.company,
            status=BaseStatus.ACTIVE.name
        )

        if supplier_id:
            queryset = queryset.filter(
                partner__id=supplier_id,
                type=BankAccountType.PARTNER.name
            )
        else:
            queryset = queryset.filter(
                type=BankAccountType.INTERNAL.name
            )
        
        return queryset

    def get_bank(self, obj, context):
        return obj.bank.code
