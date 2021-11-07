from rest_framework.response import Response
from core.utils.viewsets import ModelViewSet
from core.views_api import DataTableView, DataAsyncSearchView
from core.constants import BaseStatus
from employee.models import Department
from .serializers import *

class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(employee__id=pk)
        empl = Employee.objects.get(pk=pk)
        empl.delete()
        user.delete()

        return Response(status=200)

class EmployeeTableView(DataTableView):
    model = Employee
    order_by = '-user.update_date'
    columns_def = [
        {
            'name': 'code',
            'title': 'Mã',
            'width': '12%'
        },
        {
            'name': 'name',
            'source': 'user.display',
            'title': 'Tên',
            'width': '15%'
        },
        {
            'name': 'department',
            'display_field': 'name',
            'orderable': False,
            'title': 'Phòng/ban',
            'width': '15%'
        },
        {
            'name': 'email',
            'source': 'user.email',
            'title': 'Email',
            'width': '15%'
        },
        {
            'name': 'phone',
            'source': 'user.phone',
            'title': 'Số điện thoại',
            'width': '13%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(excludes=[BaseStatus.DRAFT.name]),
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

    def get_status(self, obj, context):
        if obj.user.is_active:
            return BaseStatus.ACTIVE.name
        else:
            return BaseStatus.INACTIVE.name

    def get_queryset(self, user):
        return Employee.objects.filter(company=user.employee.company)

class DepartmentAsyncSearchView(DataAsyncSearchView):
    model = Department
    fields = ['name']