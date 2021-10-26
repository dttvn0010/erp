from django.db.models import Q
from core.views_api import AsyncSearchView
from .models import Account, BankAccount

class AccountAsyncSearchView(AsyncSearchView):
    fields = ['code', 'name']

    def get_queryset(self, term, request):
        return Account.objects.filter(
            Q(name__icontains=term) |
            Q(code__icontains=term),
            company=request.user.employee.company,
        ).order_by('code')

class BankAccountAsyncSearchView(AsyncSearchView):
    fields = ['name', 'bank', 'account_number', 'account_holder']

    def get_queryset(self, term, request):
        bank_id = request.GET.get('bank_id')
        
        queryset =  BankAccount.objects.filter(
            Q(name__icontains=term) |
            Q(account_number__icontains=term) |
            Q(account_holder__icontains=term),
            company=request.user.employee.company,
        )

        if bank_id :
            queryset = queryset.filter(bank__id=bank_id)

        return queryset

    def get_bank(self, obj):
        return obj.bank.code