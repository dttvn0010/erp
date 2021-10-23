from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.views_api import DataTableView
from core.constants import BaseStatus
from .serializers import *

def list_location(request):
    return render(request, 'location/list.html')

class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class LocationTableView(DataTableView):
    model = Location
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '30%'
        },
        {
            'name': 'address',
            'title': 'Địa chỉ',
            'width': '35%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'edit_list': BaseStatus.choices(excludes=[BaseStatus.DRAFT.name]),
            'title': 'Trạng thái',
            'orderable': False,
            'editable': True,
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
        return Location.objects.filter(company=user.employee.company)

@api_view(['POST'])
def change_location_status(request, pk):
    location = get_object_or_404(Location, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if location.status != BaseStatus.ACTIVE.name:
        location.status = BaseStatus.ACTIVE.name
    else:
        location.status = BaseStatus.INACTIVE.name

    location.save()
    return Response({'success': True})