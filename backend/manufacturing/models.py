from django.db import models
from core.models import Company, Role
from employee.models import Employee
from stock.models import Product
from core.constants import BaseStatus

from .constants import (
    ProductionStepStatus, 
    WorkCenterState, 
    ProductionProcessStatus,
    DeviceMaintainanceStatus
)

# Create your models here.
class ProductBom(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class ProductBomItem(models.Model):
    bom = models.ForeignKey(ProductBom, related_name='items', on_delete=models.CASCADE)
    component = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    sequence = models.IntegerField()

class WorkCenter(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    working_state = models.CharField(choices=WorkCenterState.choices(), 
        default=WorkCenterState.NORMAL.name,
        max_length=50
    )

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class DeviceCategory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    parent = models.ForeignKey('DeviceCategory', 
        blank=True, null=True, 
        on_delete=models.SET_NULL
    )
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class DeviceClass(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    category = models.ForeignKey(DeviceCategory, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    hours_to_be_maintained = models.FloatField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class Device(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    workcenter = models.ForeignKey(WorkCenter, on_delete=models.PROTECT)
    _class = models.ForeignKey(DeviceClass, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    
    hours_since_last_maintainance = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class DeviceMaintainance(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    
    planned_start_date = models.DateTimeField()
    planned_end_date = models.DateTimeField()
    
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=DeviceMaintainanceStatus.choices(), 
        default=DeviceMaintainanceStatus.DRAFT.name, 
        max_length=50
    )

class ProductionWorkflow(models.Model):
    bom = models.ForeignKey(ProductBom, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class ProductionWorkflowStep(models.Model):
    workflow = models.ForeignKey(ProductionWorkflow, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    sequence = models.IntegerField()
    workcenter = models.ForeignKey(WorkCenter, on_delete=models.PROTECT)
    prior_steps = models.ManyToManyField('ProductionWorkflowStep', blank=True)

    def __str__(self):
        return self.name

class ProductionWorkflowStepDeviceUse(models.Model):
    step = models.ForeignKey(ProductionWorkflowStep, related_name='device_uses', on_delete=models.CASCADE)
    device_class = models.ForeignKey(DeviceClass, on_delete=models.PROTECT)
    hour_per_unit = models.FloatField(blank=True, null=True)
    hour_offset = models.FloatField(default=0)

class ProductionWorkflowStepEmployeeUse(models.Model):
    step = models.ForeignKey(ProductionWorkflowStep, related_name='employee_roles', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    description = models.CharField(max_length=500, blank=True)
    hour_per_unit = models.IntegerField(blank=True, null=True)
    hour_offset = models.FloatField(default=0)

class ProductionProcess(models.Model):
    bom = models.ForeignKey(ProductBom, on_delete=models.PROTECT)
    workflow = models.ForeignKey(ProductionWorkflow, blank=True, null=True, on_delete=models.PROTECT)
    product_qty = models.IntegerField()

    planned_start_date = models.DateTimeField()
    planned_end_date = models.DateTimeField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    status = models.CharField(choices=ProductionProcessStatus.choices(), 
        default=ProductionProcessStatus.DRAFT.name, 
        max_length=50
    )

    def __str__(self):
        return self.workflow.name

class ProductionStep(models.Model):
    production = models.ForeignKey(ProductionProcess, related_name='steps', on_delete=models.CASCADE)
    workflow_step = models.ForeignKey(ProductionWorkflowStep, on_delete=models.PROTECT)

    planned_start_date = models.DateTimeField(blank=True, null=True)
    planned_end_date = models.DateTimeField(blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(choices=ProductionStepStatus.choices(), 
        default=ProductionStepStatus.NEW.name,
        max_length=50)

    def __str__(self):
        return self.workflow_step.name

class ProductionStepDeviceUse(models.Model):
    step = models.ForeignKey(ProductionStep, related_name='device_uses', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)

class ProductionStepEmployeeUse(models.Model):
    workflow_role = models.ForeignKey(Role, on_delete=models.PROTECT)
    step = models.ForeignKey(ProductionStep, related_name='employee_roles', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
