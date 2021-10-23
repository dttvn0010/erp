from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _

from core.views_api import DataTableView, AsyncSearchView
from core.constants import BaseStatus
from core.views import has_permission_func
from .forms import *

class ProductTableView(DataTableView):
    model = Product
    order_by = '-update_date'
    columns_def = [
        {
            'name': 'category',
            'display_field': 'name',
            'title': 'Nhóm',
            'width': '32%',
        },
        {
            'name': 'name',
            'title': 'Tên',
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

    def get_queryset(self, user):
        return Product.objects.filter(company=user.employee.company)

# Create your views here.
def list_product(request):
    return render(request, 'product/list.html')

def edit_product(request, instance=None):
    company = request.user.employee.company
    form = ProductForm(company=company, instance=instance)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, company=company, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.company = company
            instance.save()
            return redirect('/stock/product')

    context = {'form': form}

    return render(request, 'product/form.html', context)

def create_product(request):
    return edit_product(request)

def update_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    return edit_product(request, instance)

@require_http_methods(["POST"])
@user_passes_test(has_permission_func('stock.delete_product'))
def delete_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    instance.delete()
    return HttpResponse({'success': True})

class ProductCategoryAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return ProductCategory.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )
