from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView
from .serializers import *

class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class AccountTableView(DataTableView):
    model = Account
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'code',
            'title': 'Mã',
            'width': '20%'
        },
        {
            'name': 'name',
            'title': 'Tên',
            'width': '25%'
        },
        {
            'name': 'english_name',
            'title': 'Tên tiếng Anh',
            'width': '25%'
        },
        {
            'name': 'balance',
            'title': 'Số dư',
            'width': '25%'
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
        return Account.objects.filter(company=user.employee.company)