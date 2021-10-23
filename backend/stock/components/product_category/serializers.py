from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField
from stock.models import ProductCategory

class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    parent_name = CharField(read_only=True, source='parent.name')
    parent_obj = SerializerMethodField()

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)

    def get_parent_obj(self, obj):
        if obj and obj.parent:
            return {
                'id': obj.parent.id,
                'name': obj.parent.name
            }