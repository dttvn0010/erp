from django.db import models
from core.models import Company
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
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class ProductionWorkflowStep(models.Model):
    process = models.ForeignKey(ProductionWorkflow, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    duration = models.FloatField()

    sequence = models.IntegerField()
    workcenter = models.ForeignKey(WorkCenter, on_delete=models.PROTECT)
    prior_steps = models.ManyToManyField('ProductionWorkflowStep')

    def __str__(self):
        return self.name

class ProductionWorkflowStepDeviceUse(models.Model):
    step = models.ForeignKey(ProductionWorkflowStep, on_delete=models.PROTECT)
    device = models.ForeignKey(DeviceClass, on_delete=models.PROTECT)
    duration = models.FloatField()

class ProductionProcess(models.Model):
    workflow = models.ForeignKey(ProductionWorkflow, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
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
    production = models.ForeignKey(ProductionProcess, on_delete=models.PROTECT)
    workflow_step = models.ForeignKey(ProductionWorkflowStep, on_delete=models.PROTECT)
    devices = models.ManyToManyField(Device)
    start_date = models.DateTimeField()
    planned_end_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    effective_duration = models.FloatField()
    status = models.CharField(choices=ProductionStepStatus.choices(), 
        default=ProductionStepStatus.NEW.name,
        max_length=50)

    def __str__(self):
        return self.workflow_step.name