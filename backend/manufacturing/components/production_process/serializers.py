from datetime import datetime

from rest_framework.serializers import (
    CharField, 
    PrimaryKeyRelatedField,
    IntegerField,
    DateTimeField,
    SerializerMethodField,
    ModelSerializer
)

from core.constants import BaseStatus

from manufacturing.models import (
    ProductionProcess,
    ProductionStep,
    ProductionStepDeviceUse,
    ProductionStepEmployeeUse
)

from manufacturing.constants import (
    ProductionStepStatus, 
    ProductionProcessStatus,
)

class ProductionStepDeviceUseSerializer(ModelSerializer):
    class Meta:
        model = ProductionStepDeviceUse
        fields = ['step', 'device', 'device_obj', 'device_class', 'device_class_obj']

    step = PrimaryKeyRelatedField(required=False,
        queryset=ProductionStep.objects.all()
    )

    device_obj = SerializerMethodField()
    device_class = SerializerMethodField()
    device_class_obj = SerializerMethodField()

    def get_device_obj(self, obj):
        if obj and obj.device:
            return {
                'id': obj.device.id,
                'name': obj.device.name
            }

    def get_device_class(self, obj):
        if obj and obj.device:
            return obj.device._class.pk

    def get_device_class_obj(self, obj):
        if obj and obj.device and obj.device._class:
            device_class = obj.device._class
            return {
                'id': device_class.id,
                'name': device_class.name
            }

class ProductionStepEmployeeUseSerializer(ModelSerializer):
    class Meta:
        model = ProductionStepEmployeeUse
        fields = ['step', 'workflow_role', 'workflow_role_obj', 'employee', 'employee_obj']

    step = PrimaryKeyRelatedField(required=False,
        queryset=ProductionStep.objects.all()
    )

    workflow_role_obj = SerializerMethodField()
    employee_obj = SerializerMethodField()

    def get_workflow_role_obj(self, obj):
        if obj and obj.workflow_role:
            return {
                'id': obj.workflow_role.id,
                'name': obj.workflow_role.name
            }

    def get_employee_obj(self, obj):
        if obj and obj.employee:
            return {
                'id': obj.employee.id,
                'name': obj.employee.name
            }

class ProductionStepSerializer(ModelSerializer):
    class Meta:
        model = ProductionStep
        fields = [
            'production', 'workflow_step', 'workflow_step_obj', 'device_uses', 'employee_uses',
            'planned_start_date', 'planned_end_date'
        ]

    production = PrimaryKeyRelatedField(required=False, 
        queryset=ProductionProcess.objects.all()
    )
    
    planned_start_date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])
    planned_end_date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])

    workflow_step_obj = SerializerMethodField()
    device_uses = ProductionStepDeviceUseSerializer(many=True, required=False)
    employee_uses = ProductionStepEmployeeUseSerializer(many=True, required=False)

    def get_workflow_step_obj(self, obj):
        if obj and obj.workflow_step:
            return {
                'id': obj.workflow_step.id,
                'name': obj.workflow_step.name,
            }

class ProductionProcessSerializer(ModelSerializer):
    class Meta:
        model = ProductionProcess
        fields = [
            'id', 'product', 'product_obj', 
            'bom', 'bom_obj', 'workflow', 'workflow_obj', 'product_qty',
            'planned_start_date', 'planned_end_date', 'status', 'steps'
        ]

    product = SerializerMethodField()
    product_obj = SerializerMethodField()
    bom_obj = SerializerMethodField()
    workflow_obj = SerializerMethodField()

    planned_start_date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])
    planned_end_date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])

    status = CharField(read_only=True)
    steps = ProductionStepSerializer(many=True, required=False)

    def get_product(self, obj):
        if obj and obj.bom and obj.bom.product:
            return obj.bom.product.id

    def get_product_obj(self, obj):
        if obj and obj.bom and obj.bom.product:
            product = obj.bom.product
            return {
                'id': product.id,
                'name': product.name
            }

    def get_bom_obj(self, obj):
        if obj and obj.bom:
            return {
                'id': obj.bom.id,
                'name': obj.bom.name,
            }

    def get_workflow_obj(self, obj):
        if obj and obj.workflow:
            return {
                'id': obj.workflow.id,
                'name': obj.workflow.name,
            }

    def create_step(self, production, validated_step_data):
        device_uses_data = validated_step_data.pop('device_uses', [])
        employee_uses_data = validated_step_data.pop('employee_uses', [])
        
        validated_step_data['production'] = production

        step = ProductionStep.objects.create(
            **validated_step_data,
            status=ProductionStepStatus.NEW.name
        )

        for device_use_data in device_uses_data:
            device_use_data['step'] = step
            ProductionStepDeviceUse.objects.create(
                **device_use_data
            )
        
        for employee_use_data in employee_uses_data:
            employee_use_data['step'] = step
            ProductionStepEmployeeUse.objects.create(
                **employee_use_data
            )

        return step
        
    def create(self, validated_data):

        steps_data = validated_data.pop('steps', [])

        production = ProductionProcess.objects.create(
            **validated_data,
            status=ProductionProcessStatus.DRAFT.name
        )

        for step_data in steps_data:
            self.create_step(production, step_data)

        return production

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])

        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()

        for step in instance.steps.all():
            step.delete()

        for step_data in steps_data:
            self.create_step(instance, step_data)

        return instance