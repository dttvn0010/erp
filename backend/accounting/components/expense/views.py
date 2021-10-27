from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView, AsyncSearchView
from core.constants import BaseStatus
from accounting.models import ExpenseType
from .serializers import *


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class ExpenseTableView(DataTableView):
    model = Expense
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'amount',
            'source': 'ledger.amount',
            'title': 'Số tiền',
            'width': '15%'
        },
        {
            'name': 'payment_type',
            'source': 'ledger.cash',
            'display_list': [
                (True, 'Tiền mặt'),
                (False, 'Chuyển khoản')
            ],
            'title': 'Hình thức thanh toán',
            'width': '15%'
        },
        {
            'name': 'note',
            'source': 'ledger.memo',
            'title': 'Ghi chú',
            'width': '25%'
        },
        {
            'name': 'date',
            'source': 'approve_date',
            'format': '%d/%m/%Y %H:%M:%S',
            'title': 'Ngày chi',
            'width': '15%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'title': 'Trạng thái',
            'orderable': False,
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

    def filter_by_payment_type(self, queryset, value):
        value = map(lambda x: x == 'true', value.split(','))
        return queryset.filter(ledger__cash__in=value)

    def get_queryset(self, user):
        return Expense.objects.filter(company=user.employee.company)


class ExpenseTypeAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return ExpenseType.objects.filter(
            company=request.user.employee.company,
            name__icontains=term
        )

@api_view(['GET'])
def get_expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    data = ExpenseSerializer(expense).data
    #items = ExpenseItem.objects.filter(expense=expense)
    #data['items'] = ExpenseItemSerializer(items, many=True).data
    return Response(data)

@api_view(['POST'])
def add_expense_item(request, pk):
    data = request.data
    serializer = ExpenseItemSerializer(data={**data, 'expense': pk})
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def save_expense(request, pk):
    ...