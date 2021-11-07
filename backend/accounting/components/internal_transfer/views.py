from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView
from core.constants import BaseStatus
from accounting.constants import BankAccountType
from .serializers import *

class InternalTransferViewSet(ModelViewSet):
    serializer_class = InternalTransferSerializer
    queryset = InternalTransfer.objects.all()

class InternalTransferTableView(DataTableView):
    model = InternalTransfer
    order_by = '-update_date'
    columns_def = [
        
        {
            'name': 'amount',
            'source': 'ledger.amount',
            'title': 'Số tiền',
            'search': False,
            'width': '12%'
        },
        
         {
            'name': 'from_bank_account',
            'source': 'ledger.from_bank_account',
            'display_field': 'name',
            'search_options': {
                #'async': True,
                'extra_filters': {
                    #'type': BankAccountType.INTERNAL.name
                }
            },
            'title': 'Tài khoản chuyển tiền',
            'width': '15%'
        },

        {
            'name': 'to_bank_account',
            'source': 'ledger.to_bank_account',
            'display_field': 'name',
            'search_options': {
                #'async': True,
                'extra_filters': {
                    #'type': BankAccountType.INTERNAL.name
                }
            },
            'title': 'Tài khoản nhận tiền',
            'width': '15%'
        },

        {
            'name': 'note',
            'source': 'ledger.memo',
            'title': 'Ghi chú',
            'orderable': False,
            'width': '20%'
        },
        {
            'name': 'date',
            'format': '%d/%m/%Y %H:%M:%S',
            'title': 'Ngày chuyển',
            'width': '13%'
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
        return InternalTransfer.objects.filter(company=user.employee.company)
