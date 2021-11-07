from rest_framework.serializers import CharField
from core.utils.serializers import ModelSerializer
from accounting.models import ExpenseType

class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name', 'status', 'description']

    status = CharField(read_only=True)