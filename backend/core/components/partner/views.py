from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.views_api import DataTableView
from core.constants import BaseStatus
from .serializers import *

class PartnerViewSet(ModelViewSet):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class PartnerTableView(DataTableView):
    model = Partner
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '15%'
        },
        {
            'name': 'phone',
            'title': 'Số điện thoại',
            'width': '15%'
        },
        {
            'name': 'address',
            'title': 'Địa chỉ',
            'width': '24%'
        },
        {
            'name': 'is_supplier',
            'title': 'Là nhà cung cấp',
            'orderable': False,
            'css_class': 'text-center',
            'is_narrow': True,
            'width': '7%'
        },
        {
            'name': 'is_customer',
            'title': 'Là khách hàng',
            'orderable': False,
            'css_class': 'text-center',
            'is_narrow': True,
            'width': '7%'
        },
        {
            'name': 'is_agent',
            'title': 'Là đại lý',
            'orderable': False,
            'css_class': 'text-center',
            'is_narrow': True,
            'width': '7%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'edit_list': BaseStatus.choices(excludes=[BaseStatus.DRAFT.name]),
            'title': 'Trạng thái',
            'orderable': False,
            'editable': True,
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
        return Partner.objects.filter(company=user.staff.company)

@api_view(['POST'])
def change_partner_status(request, pk):
    partner = get_object_or_404(Partner, 
        pk=pk,
        company= request.user.staff.company
    )
    
    if partner.status != BaseStatus.ACTIVE.name:
        partner.status = BaseStatus.ACTIVE.name
    else:
        partner.status = BaseStatus.INACTIVE.name

    partner.save()
    return Response({'success': True})