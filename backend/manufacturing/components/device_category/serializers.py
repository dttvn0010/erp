from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import  CharField
from core.utils.serializers import ModelSerializer

from manufacturing.models import DeviceCategory

class DeviceCategorySerializer(ModelSerializer):
    class Meta:
        model = DeviceCategory
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
    parent_obj = SerializerMethodField()

    def get_parent_obj(self, obj):
        if obj and obj.parent:
            return {
                'id': obj.parent.id,
                'name': obj.parent.name
            }