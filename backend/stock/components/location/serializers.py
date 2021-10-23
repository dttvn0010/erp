from rest_framework.serializers import ModelSerializer, CharField
from stock.models import Location

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'status']

    status = CharField(read_only=True)

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)