from rest_framework.serializers import ModelSerializer, CharField
from stock.models import ProductCategory

class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    parent_name = CharField(read_only=True, source='parent.name')

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].staff.company
        return super().create(validated_data)