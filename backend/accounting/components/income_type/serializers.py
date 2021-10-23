from rest_framework.serializers import ModelSerializer, CharField
from accounting.models import IncomeType

class IncomeTypeSerializer(ModelSerializer):
    class Meta:
        model = IncomeType
        fields = ['id', 'name', 'status', 'description']

    status = CharField(read_only=True)

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)