from rest_framework.serializers import CharField
from core.utils.serializers import ModelSerializer
from stock.models import Location

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'status']

    status = CharField(read_only=True)