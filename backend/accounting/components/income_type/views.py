from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView
from core.constants import BaseStatus
from .serializers import *

class IncomeTypeViewSet(ModelViewSet):
    serializer_class = IncomeTypeSerializer
    queryset = IncomeType.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class IncomeTypeTableView(DataTableView):
    model = IncomeType
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
        return IncomeType.objects.filter(company=user.employee.company)

@api_view(['POST'])
def change_income_type_status(request, pk):
    income_type = get_object_or_404(IncomeType, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if income_type.status != BaseStatus.ACTIVE.name:
        income_type.status = BaseStatus.ACTIVE.name
    else:
        income_type.status = BaseStatus.INACTIVE.name

    income_type.save()
    return Response({'success': True})