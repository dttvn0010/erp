from core.utils.viewsets import ModelViewSet
from core.views_api import ChangeItemStatusView
from core.constants import BaseStatus

from .serializers import *

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ChangeProductStatusView(ChangeItemStatusView):
    model = Product