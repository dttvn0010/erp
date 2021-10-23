from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView
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

@api_view(['POST'])
def change_bank_status(request, pk):
    bank = get_object_or_404(Bank, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if bank.status != BaseStatus.ACTIVE.name:
        bank.status = BaseStatus.ACTIVE.name
    else:
        bank.status = BaseStatus.INACTIVE.name

    bank.save()
    return Response({'success': True})