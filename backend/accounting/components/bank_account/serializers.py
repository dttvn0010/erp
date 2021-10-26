from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from accounting.models import BankAccount

class BankSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'bank', 'bank_obj', 'bank_branch', 'account_number', 'account_holder']

    bank_obj = SerializerMethodField()

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)

    def get_bank_obj(self, obj):
        if obj and obj.bank:
            return {
                'id': obj.bank.id,
                'name': obj.bank.name
            }