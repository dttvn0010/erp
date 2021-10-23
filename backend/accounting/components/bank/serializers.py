from rest_framework.serializers import ModelSerializer
from accounting.models import Bank

class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'code', 'name', 'logo']

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)