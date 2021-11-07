from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import CharField
from core.utils.serializers import ModelSerializer
from stock.models import ProductCategory

class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    parent_name = CharField(read_only=True, source='parent.name')
    parent_obj = SerializerMethodField()

    def get_parent_obj(self, obj):
        if obj and obj.parent:
            return {
                'id': obj.parent.id,
                'name': obj.parent.name
            }