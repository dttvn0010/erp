from rest_framework.viewsets import ModelViewSet
from stock.models import Export
from .serializers import *

class ExportViewSet(ModelViewSet):
    serializer_class = ExportSerializer
    queryset = Export.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context