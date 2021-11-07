from core.utils.serializers import ModelSerializer
from accounting.models import Bank

class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'code', 'name', 'logo']