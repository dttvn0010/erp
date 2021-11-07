from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView, ChangeItemStatusView
from core.constants import BaseStatus
from .serializers import *

class BankViewSet(ModelViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class BankTableView(DataTableView):
    model = Bank
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'logo',
            'title': 'Logo',
            'css_class': 'text-center',
            'width': '10%',
        },
        {
            'name': 'code',
            'title': 'Tên viết tắt',
            'width': '15%'
        },
        {
            'name': 'name',
            'title': 'Tên đầy đủ',
            'width': '40%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
            'width': '30%'
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
        return Bank.objects.filter(company=user.employee.company)

class ChangeBankStatusView(ChangeItemStatusView):
    model = Bank