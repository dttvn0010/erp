from datetime import datetime

from rest_framework.serializers import (
    CharField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField,
    ModelSerializer
)

from core.constants import BaseStatus

from manufacturing.models import (
    ProductionWorkflow, 
    ProductionWorkflowStep,
    ProductionWorkflowStepDeviceUse,
    ProductionWorkflowStepEmployeeUse
)

class ProductionWorkflowStepDeviceUseSerializer(ModelSerializer):
    class Meta:
        model = ProductionWorkflowStepDeviceUse
        fields = ['step', 'device_class', 'device_class_obj', 'hour_per_unit', 'hour_offset']

    step = PrimaryKeyRelatedField(required=False,
        queryset=ProductionWorkflowStep.objects.all()
    )

    device_class_obj = SerializerMethodField()

    def get_device_class_obj(self, obj):
        if obj and obj.device_class:
            return {
                'id': obj.device_class.id,
                'name': obj.device_class.name
            }

class ProductionWorkflowStepEmployeeUseSerializer(ModelSerializer):
    class Meta:
        model = ProductionWorkflowStepEmployeeUse
        fields = ['step', 'role', 'role_obj', 'hour_per_unit', 'hour_offset']

    step = PrimaryKeyRelatedField(required=False,
        queryset=ProductionWorkflowStep.objects.all()
    )

    role_obj = SerializerMethodField()

    def get_role_obj(self, obj):
        if obj and obj.role:
            return {
                'id': obj.role.id,
                'name': obj.role.name
            }

class ProductionWorkflowStepSerializer(ModelSerializer):
    class Meta:
        model = ProductionWorkflowStep
        fields = ['id', 'workflow', 'name', 'workcenter', 'workcenter_obj', 'device_uses', 'employee_uses', 'sequence']

    workflow = PrimaryKeyRelatedField(required=False, 
        queryset=ProductionWorkflow.objects.all()
    )
    
    sequence = IntegerField(required=False)
    workcenter_obj = SerializerMethodField()
    device_uses = ProductionWorkflowStepDeviceUseSerializer(many=True, required=False)
    employee_uses = ProductionWorkflowStepEmployeeUseSerializer(many=True, required=False)

    def get_workcenter_obj(self, obj):
        if obj and obj.workcenter:
            return {
                'id': obj.workcenter.id,
                'name': obj.workcenter.name,
            }

class ProductionWorkflowSerializer(ModelSerializer):
    class Meta:
        model = ProductionWorkflow
        fields = [
            'id', 'bom', 'bom_obj', 'name', 'status', 'steps'
        ]

    bom_obj = SerializerMethodField()
    status = CharField(read_only=True)
    steps = ProductionWorkflowStepSerializer(many=True, required=False)

    def get_bom_obj(self, obj):
        if obj and obj.bom:
            return {
                'id': obj.bom.id,
                'name': obj.bom.name,
            }

    def create_step(self, workflow, validated_step_data):
        device_uses_data = validated_step_data.pop('device_uses', [])
        employee_uses_data = validated_step_data.pop('employee_uses', [])
        
        validated_step_data['workflow'] = workflow

        step = ProductionWorkflowStep.objects.create(
            **validated_step_data
        )

        for device_use_data in device_uses_data:
            device_use_data['step'] = step
            ProductionWorkflowStepDeviceUse.objects.create(
                **device_use_data
            )
        
        for employee_use_data in employee_uses_data:
            employee_use_data['step'] = step
            ProductionWorkflowStepEmployeeUse.objects.create(
                **employee_use_data
            )

        return step
        
    def create(self, validated_data):

        steps_data = validated_data.pop('steps', [])

        workflow = ProductionWorkflow.objects.create(
            **validated_data,
            status=BaseStatus.DRAFT.name
        )

        for i, step_data in enumerate(steps_data):
            step_data['sequence'] = i + 1
            self.create_step(workflow, step_data)

        return workflow

    def update(self, instance, validated_data):
        if instance.status == BaseStatus.ACTIVE.name:
            instance.name = validated_data['name']
            instance.save()
            return instance

        steps_data = validated_data.pop('steps', [])
        instance.name = validated_data['name']
        instance.bom = validated_data['bom']
        instance.save()

        for step in instance.steps.all():
            step.delete()

        for i,step_data in enumerate(steps_data):
            step_data['sequence'] = i + 1
            self.create_step(instance, step_data)

        return instance