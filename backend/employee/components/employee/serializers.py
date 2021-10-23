from rest_framework.serializers import ModelSerializer, CharField
from employee.models import Employee

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'code', 'name', 'phone', 'email', 'department', 'department_name', 'status']

    name = CharField(read_only=True, source='user.display')
    phone = CharField(read_only=True, source='user.phone')
    email = CharField(read_only=True, source='user.email')
    department_name = CharField(read_only=True, source='department.name')
    status = CharField(read_only=True)

    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)
