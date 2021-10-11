from rest_framework.serializers import ModelSerializer, CharField
from core.models import Partner

class PartnerSerializer(ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'email', 'phone', 'address',
                    'is_supplier', 'is_customer', 'is_agent', 'status']

    status = CharField(read_only=True)

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].staff.company
        return super().create(validated_data)