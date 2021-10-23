from rest_framework.serializers import ModelSerializer
from accounting.models import Account

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'code', 'name', 'english_name', 'balance']

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)