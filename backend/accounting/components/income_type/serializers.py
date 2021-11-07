from rest_framework.serializers import CharField
from core.utils.serializers import ModelSerializer
from accounting.models import IncomeType

class IncomeTypeSerializer(ModelSerializer):
    class Meta:
        model = IncomeType
        fields = ['id', 'name', 'status', 'description']

    status = CharField(read_only=True)