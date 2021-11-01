from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField
from manufacturing.models import DeviceCategory

class DeviceCategorySerializer(ModelSerializer):
    class Meta:
        model = DeviceCategory
        exclude = ['company', 'create_date', 'update_date']

    status = CharField(read_only=True)
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