from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, AsyncSearchView

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

@api_view(['POST'])
def change_device_category_status(request, pk):
    category = get_object_or_404(DeviceCategory, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if category.status != BaseStatus.ACTIVE.name:
        category.status = BaseStatus.ACTIVE.name
    else:
        category.status = BaseStatus.INACTIVE.name

    category.save()
    return Response({'success': True})