from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.utils.translation import gettext as _

from core.views_api import DataTableView, AsyncSearchView
from core.constants import BaseStatus
from core.views import has_permission_func
from .forms import *

class ProductCategoryTableView(DataTableView):
    model = ProductCategory
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'parent',
            'display_field': 'name',
            'title': 'Nhóm cha',
            'width': '32%',
        },
        {
            'name': 'name',
            'title': 'Tên nhóm',
            'width': '32%'
        },
        {
            'name': 'status',
            'display_list': BaseStatus.choices(),
            'edit_list': BaseStatus.choices(excludes=[BaseStatus.DRAFT.name]),
            'title': 'Trạng thái',
            'orderable': False,
            'editable': True,
            'width': '32%'
        },
        {
            'title': 'Thao tác',
            'orderable': False,
            'search': False,
            'css_class': 'text-center',
            'width': '5%'
        },
    ]

    def user_can_edit(self, user):
        return False #return has_permission(user, 'stock.change_productcategory')

    def get_queryset(self, user):
        return ProductCategory.objects.filter(company=user.employee.company)

# Create your views here.
def list_product_category(request):
    return render(request, 'product_category/list.html')

def edit_product_category(request, instance=None):
    company = request.user.employee.company
    form = ProductCategoryForm(company=company, instance=instance)
    
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, company=company, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.company = company
            instance.save()
            return redirect('/stock/product-category')

    context = {'form': form}

    return render(request, 'product_category/form.html', context)

def create_product_category(request):
    return edit_product_category(request)

def update_product_category(request, pk):
    instance = get_object_or_404(ProductCategory, pk=pk)
    return edit_product_category(request, instance)

@require_http_methods(["POST"])
@user_passes_test(has_permission_func('stock.delete_productcategory'))
def delete_product_category(request, pk):
    instance = get_object_or_404(ProductCategory, pk=pk)
    instance.delete()
    return HttpResponse({'success': True})

class ParentAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        print('data=', request.GET)
        instanceId = request.GET.get('instanceId')

        queryset = ProductCategory.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

        if instanceId:
            queryset = queryset.filter(~Q(pk=instanceId)) \
                                .filter(~Q(parent__id=instanceId))
        
        return queryset