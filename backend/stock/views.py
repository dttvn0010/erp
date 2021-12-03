from core.views_api import AsyncSearchView
from stock.models import Location, Product, ProductQuantity
from core.constants import BaseStatus

class ProductAsyncSearchView(AsyncSearchView):
    fields = ['name', 'cur_stock_qty']

    def get_context(self, request):
        context = {}
        location_id = request.GET.get('location_id')
        
        if location_id:
            context['location'] = Location.objects.filter(pk=location_id).first()

        return context
            
    def get_cur_stock_qty(self, obj, context):
        if not context.get('location'):
            return None
        
        location = context['location']
        product_qty = ProductQuantity.objects.filter(
            product=obj,
            location=location,
            is_latest=True
        ).first()

        return product_qty.qty if product_qty else 0

    def get_queryset(self, term, request):
        return Product.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )

class LocationAsyncSearchView(AsyncSearchView):
    fields = ['name']

    def get_queryset(self, term, request):
        return Location.objects.filter(
            company=request.user.employee.company,
            name__icontains=term,
            status=BaseStatus.ACTIVE.name
        )