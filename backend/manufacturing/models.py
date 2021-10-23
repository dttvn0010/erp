from django.db import models
from core.models import Company
from stock.models import Product
from core.constants import BaseStatus
from .constants import ProductionStepStatus, WorkCenterState, ProductionProcessStatus

# Create your models here.
class ProductBom(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class ProductBomItem(models.Model):
    bom = models.ForeignKey(ProductBom, on_delete=models.PROTECT)
    component = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    sequence = models.IntegerField()

class WorkCenter(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    working_state = models.CharField(choices=WorkCenterState.choices(), max_length=50)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class DeviceCategory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

class DeviceTemplate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    category = models.ForeignKey(DeviceCategory, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    hours_to_be_maintained = models.FloatField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class Device(models.Model):
    workcenter = models.ForeignKey(WorkCenter, on_delete=models.PROTECT)
    template = models.ForeignKey(DeviceTemplate, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    
    hours_since_last_maintainance = models.FloatField()
    total_hours = models.FloatField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class DeviceMaintainance(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

class ProductionWorkflow(models.Model):
    bom = models.ForeignKey(ProductBom, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), max_length=50)

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
    device = models.ForeignKey(DeviceTemplate, on_delete=models.PROTECT)
    duration = models.FloatField()

class ProductionProcess(models.Model):
    workflow = models.ForeignKey(ProductionWorkflow, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    planned_end_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ProductionProcessStatus.choices(), max_length=50)

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
    status = models.CharField(choices=ProductionStepStatus.choices(), max_length=50)

    def __str__(self):
        return self.workflow_step.name