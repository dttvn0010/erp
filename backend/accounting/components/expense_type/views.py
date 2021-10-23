from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView
from core.constants import BaseStatus
from .serializers import *

class ExpenseTypeViewSet(ModelViewSet):
    serializer_class = ExpenseTypeSerializer
    queryset = ExpenseType.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class ExpenseTypeTableView(DataTableView):
    model = ExpenseType
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '30%'
        },
        {
            'name': 'description',
            'title': 'Mô tả',
            'width': '35%'
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
        return ExpenseType.objects.filter(company=user.employee.company)

@api_view(['POST'])
def change_expense_type_status(request, pk):
    expense_type = get_object_or_404(ExpenseType, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if expense_type.status != BaseStatus.ACTIVE.name:
        expense_type.status = BaseStatus.ACTIVE.name
    else:
        expense_type.status = BaseStatus.INACTIVE.name

    expense_type.save()
    return Response({'success': True})