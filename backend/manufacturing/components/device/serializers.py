from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField
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

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print('validated_data=', validated_data)
        return super().update(instance, validated_data)

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