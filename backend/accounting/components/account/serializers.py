from core.utils.serializers import ModelSerializer
from accounting.models import Account

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'code', 'name', 'english_name', 'balance']