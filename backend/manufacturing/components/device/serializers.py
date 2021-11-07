from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import CharField
from core.utils.serializers import ModelSerializer
from manufacturing.models import Device

class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        exclude = ['create_date', 'update_date', 'company', 
                    'hours_since_last_maintainance', 'total_hours']

    status = CharField(read_only=True)
    class_obj = SerializerMethodField()
    workcenter_obj = SerializerMethodField()
    _class_obj = SerializerMethodField()

    def get__class_obj(self, obj):
        if obj and obj._class:
            return {
                'id': obj._class.id,
                'name': obj._class.name
            }

    def get_class_obj(self, obj):
        return self.get__class_obj(obj)

    def get_workcenter_obj(self, obj):
        if obj and obj.workcenter:
            return {
                'id': obj.workcenter.id,
                'name': obj.workcenter.name
            }