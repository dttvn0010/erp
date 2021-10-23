from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from stock.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    category_name = CharField(read_only=True, source='category.name')
    category_obj = SerializerMethodField()

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)

    def get_category_obj(self, obj):
        if obj and obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name
            }