from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField
from manufacturing.models import DeviceMaintainance

class DeviceMaintainanceSerializer(ModelSerializer):
    class Meta:
        model = DeviceMaintainance
        exclude = ['create_date', 'update_date']

    planned_start_date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])
    planned_end_date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])

    start_date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M')
    end_date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M')

    status = CharField(read_only=True)
    device_obj = SerializerMethodField()

    def get_device_obj(self, obj):
        if obj and obj.device:
            return {
                'id': obj.device.id,
                'name': obj.device.name
            }