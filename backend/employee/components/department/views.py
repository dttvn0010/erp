from django.shortcuts import get_object_or_404
from django.db.models import Q 

from rest_framework.viewsets import ModelViewSet
from core.views_api import DataTableView, AsyncSearchView, ChangeItemStatusView
from core.constants import BaseStatus
from employee.models import Employee
from .serializers import *

class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        department = get_object_or_404(Department, pk=pk)
        
        for empl in Employee.objects.filter(department=department):
            empl.department = None
            empl.save()

        return super().destroy(request, *args, **kwargs)
        
class DepartmentTableView(DataTableView):
    model = Department
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'name',
            'title': 'Tên',
            'width': '22%'
        },
        {
            'name': 'parent',
            'display_field': 'name',
            'title': 'Trực thuộc',
            'width': '22%'
        },
        {
            'name': 'manager',
            'display_field': 'user.display',
            'search_options': {
                'extra_filters': {'user__is_active': True}
            },
            'title': 'Người quản lý',
            'width': '22%'
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

    def get_queryset(self, user, params):
        return Department.objects.filter(company=user.employee.company)

class ChangeDepartmentStatusView(ChangeItemStatusView):
    model = Department

class ParentAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        instanceId = request.GET.get('instanceId')
        queryset = Department.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )
        if instanceId:
            queryset = queryset.filter(~Q(pk=instanceId)) \
                        .filter(~Q(parent__id=instanceId))
        
        return queryset

class EmployeeAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return Employee.objects.filter(
            company=request.user.employee.company,
            user__display__icontains=term,
            user__is_active=True
        )

    def get_name(self, obj, context):
        return obj.user.display