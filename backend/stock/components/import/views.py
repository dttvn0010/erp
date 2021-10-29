from rest_framework.viewsets import ModelViewSet
from stock.models import Import
from .serializers import *

class ImportViewSet(ModelViewSet):
    serializer_class = ImportSerializer
    queryset = Import.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context