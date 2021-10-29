from rest_framework.viewsets import ModelViewSet
from stock.models import Exchange
from .serializers import *

class ExchangeViewSet(ModelViewSet):
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context