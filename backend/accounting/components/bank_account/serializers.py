from rest_framework.serializers import ModelSerializer, CharField
from accounting.models import BankAccount

class BankSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'bank', 'bank_name', 'bank_branch', 'account_number', 'account_holder']

    bank_name = CharField(read_only=True, source='bank.name')

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)