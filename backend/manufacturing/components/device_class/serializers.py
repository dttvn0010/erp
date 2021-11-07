from rest_framework.serializers import CharField, SerializerMethodField
from core.utils.serializers import ModelSerializer
from manufacturing.models import DeviceClass

class DeviceClassSerializer(ModelSerializer):
    class Meta:
        model = DeviceClass
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    category_obj = SerializerMethodField()

    def get_category_obj(self, obj):
        if obj and obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name
            }