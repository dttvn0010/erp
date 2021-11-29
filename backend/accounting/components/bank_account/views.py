from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, DataAsyncSearchView, ChangeItemStatusView
from core.constants import BaseStatus
from accounting.models import Bank
from .serializers import *

class BankAccountViewSet(ModelViewSet):
    serializer_class = BankSerializer
    queryset = BankAccount.objects.all()

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

    def get_queryset(self, user, params):
        return BankAccount.objects.filter(company=user.employee.company)

class ChangeBankAccountStatusView(ChangeItemStatusView):
    model = BankAccount

class BankAsyncSearchView(DataAsyncSearchView):
    model = Bank
    fields = ['name']