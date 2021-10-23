from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus

from .serializers import *

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

@api_view(['POST'])
def change_product_status(request, pk):
    product = get_object_or_404(Product, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if product.status != BaseStatus.ACTIVE.name:
        product.status = BaseStatus.ACTIVE.name
    else:
        product.status = BaseStatus.INACTIVE.name

    product.save()
    return Response({'success': True})