from rest_framework.serializers import ModelSerializer, CharField
from accounting.models import ExpenseType

class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name', 'status', 'description']

    status = CharField(read_only=True)
    
    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)