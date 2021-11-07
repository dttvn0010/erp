from rest_framework.serializers import CharField
from core.utils.serializers import ModelSerializer
from core.models import Partner

class PartnerSerializer(ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'code', 'name', 'email', 'phone', 'address',
                    'is_supplier', 'is_customer', 'is_organization', 'status']

    status = CharField(read_only=True)