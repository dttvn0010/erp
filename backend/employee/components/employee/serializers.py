from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models import User
from employee.models import Employee

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'code', 'name', 'phone', 'email', 'department', 'department_obj', 'status']

    code = CharField()
    name = CharField(source='user.display')
    email = CharField(source='user.email')
    phone = CharField(allow_blank=True, source='user.phone')
    status = CharField(read_only=True)

    department_obj = SerializerMethodField()

    def get_department_obj(self, obj):
        if obj and obj.department:
            return {
                'id': obj.department.id, 
                'name': obj.department.name
            }

    def create(self, validated_data):
        company = self.context['user'].employee.company
        user_data = validated_data['user']
        
        user = User.objects.create_user(
            username= user_data['email'],
            email=user_data['email'],
            phone=user_data.get('phone', ''),
            display=user_data['display'],
        )

        return Employee.objects.create(
            company=company,
            code=validated_data['code'],
            department=validated_data.get('department'),
            user=user,
        )
        

    def update(self, instance, validated_data):
        print('validated_data=', validated_data)
        user_data = validated_data['user']
        user = instance.user
        user.username = user.email = user_data['email']
        user.display = user_data['display']
        user.phone = user_data.get('phone', '')
        user.save()

        instance.code=validated_data['code']
        instance.department = validated_data.get('department')
        instance.save()

        return instance
