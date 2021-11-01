from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus
from core.views_api import DataTableView, AsyncSearchView
from manufacturing.constants import WorkCenterState
from .serializers import *

class WorkCenterTableView(DataTableView):
    model = WorkCenter
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '35%'
        },
        {
            'name': 'working_state',
            'display_list': WorkCenterState.choices(),
            'title': 'Trạng thái hoạt động',
            'width': '30%'
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
        return WorkCenter.objects.filter(company=user.employee.company)

class WorkCenterViewSet(ModelViewSet):
    queryset = WorkCenter.objects.all()
    serializer_class = WorkCenterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

@api_view(['POST'])
def change_work_center_status(request, pk):
    work_center = get_object_or_404(WorkCenter, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if work_center.status != BaseStatus.ACTIVE.name:
        work_center.status = BaseStatus.ACTIVE.name
    else:
        work_center.status = BaseStatus.INACTIVE.name

    work_center.save()
    return Response({'success': True})