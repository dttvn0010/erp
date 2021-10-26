from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from employee.models import Department

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'parent_obj', 'manager', 'manager_obj', 'status']

    status = CharField(read_only=True)
    parent_obj = SerializerMethodField()
    manager_obj = SerializerMethodField()

    def get_parent_obj(self, obj):
        if obj and obj.parent:
            return {
                'id': obj.parent.id,
                'name': obj.parent.name
            }

    def get_manager_obj(self, obj):
        if obj and obj.manager:
            return {
                'id': obj.manager.id,
                'name': obj.manager.user.display
            }

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        instance = super().create(validated_data)
        
        manager = validated_data.get('manager')
        if manager:
            manager.department = instance
            manager.save()
        
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        manager = validated_data.get('manager')
        
        if manager:
            manager.department = instance
            manager.save()
        
        return instance

