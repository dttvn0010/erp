from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView, AsyncSearchView
from core.constants import BaseStatus
from accounting.models import Bank
from .serializers import *

class BankAccountViewSet(ModelViewSet):
    serializer_class = BankSerializer
    queryset = BankAccount.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class BankAccountTableView(DataTableView):
    model = BankAccount
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '15%'
        },
        {
            'name': 'bank',
            'display_field': 'name',
            'title': 'Ngân hàng',
            'width': '18%'
        },
        {
            'name': 'bank_branch',
            'title': 'Chi nhánh',
            'width': '15%'
        },
        {
            'name': 'account_number',
            'title': 'Số tài khoản',
            'width': '12%'
        },
        {
            'name': 'account_holder',
            'title': 'Chủ tài khoản',
            'width': '15%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
            'width': '20%'
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
        return BankAccount.objects.filter(company=user.employee.company)

@api_view(['POST'])
def change_bank_account_status(request, pk):
    bank_account = get_object_or_404(BankAccount, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if bank_account.status != BaseStatus.ACTIVE.name:
        bank_account.status = BaseStatus.ACTIVE.name
    else:
        bank_account.status = BaseStatus.INACTIVE.name

    bank_account.save()
    return Response({'success': True})

class BankAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return Bank.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )