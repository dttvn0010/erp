from django.db.models import manager
from rest_framework.serializers import ModelSerializer, CharField
from employee.models import Department

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'parent_name', 'manager', 'manager_name', 'status']

    status = CharField(read_only=True)
    parent_name = CharField(read_only=True, source='parent.name')
    manager_name = CharField(read_only=True, source='manager.user.display')

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