from core.utils.viewsets import ModelViewSet
from core.views_api import ChangeItemStatusView
from core.constants import BaseStatus

from .serializers import *

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ChangeProductCategoryStatusView(ChangeItemStatusView):
    model = ProductCategory