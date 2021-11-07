from core.utils.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, AsyncSearchView, ChangeItemStatusView

from .serializers import *

class DeviceCategoryTableView(DataTableView):
    model = DeviceCategory
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'parent',
            'display_field': 'name',
            'title': 'Nhóm cha',
            'width': '25%',
        },
        {
            'name': 'code',
            'title': 'Mã',
            'width': '20%'
        },
        {
            'name': 'name',
            'title': 'Tên nhóm',
            'width': '25%'
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

    def get_queryset(self, user):
        return DeviceCategory.objects.filter(company=user.employee.company)

class ParentAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        instanceId = request.GET.get('instanceId')

        queryset = DeviceCategory.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

        if instanceId:
            queryset = queryset.filter(~Q(pk=instanceId)) \
                                .filter(~Q(parent__id=instanceId))
        
        return queryset

class DeviceCategoryViewSet(ModelViewSet):
    queryset = DeviceCategory.objects.all()
    serializer_class = DeviceCategorySerializer

class ChangeDeviceCategoryStatusView(ChangeItemStatusView):
    model = DeviceCategory