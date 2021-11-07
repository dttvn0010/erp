from rest_framework.serializers import CharField, SerializerMethodField
from core.utils.serializers import ModelSerializer
from accounting.models import BankAccount

class BankSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'bank', 'bank_obj', 'bank_branch', 'account_number', 'account_holder']

    bank_obj = SerializerMethodField()

    def get_bank_obj(self, obj):
        if obj and obj.bank:
            return {
                'id': obj.bank.id,
                'name': obj.bank.name
            }