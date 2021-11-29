from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, ChangeItemStatusView
from core.constants import BaseStatus
from .serializers import *

class PartnerViewSet(ModelViewSet):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()

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
            'name': 'is_organization',
            'title': 'Là công ty',
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

    def get_queryset(self, user, params):
        return Partner.objects.filter(company=user.employee.company)

class ChangePartnerStatusView(ChangeItemStatusView):
    model = Partner