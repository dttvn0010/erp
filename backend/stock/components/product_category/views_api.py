from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from core.constants import BaseStatus

from .serializers import *

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

@api_view(['POST'])
def change_product_category_status(request, pk):
    category = get_object_or_404(ProductCategory, 
        pk=pk,
        company= request.user.employee.company
    )
    
    if category.status != BaseStatus.ACTIVE.name:
        category.status = BaseStatus.ACTIVE.name
    else:
        category.status = BaseStatus.INACTIVE.name

    category.save()
    return Response({'success': True})