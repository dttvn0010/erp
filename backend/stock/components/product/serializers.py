from rest_framework.serializers import ModelSerializer, CharField
from stock.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    category_name = CharField(read_only=True, source='category.name')

    def create(self, validated_data):
        print('validated_data=', validated_data)
        validated_data['company'] = self.context['user'].staff.company
        return super().create(validated_data)