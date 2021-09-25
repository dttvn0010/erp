from django.db import models
from django.utils.translation import gettext as _
from accounting.models import Invoice
from core.models import Company, Partner
from employee.models import Staff
from stock.models import Location, ProductMove
from .constants import OrderStatus

# Create your models here.
class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='company_purchase_orders')

    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                        blank=True, null=True, related_name='location_purchase_orders')

    supplier = models.ForeignKey(Partner, on_delete=models.PROTECT)
    order_lines = models.ManyToManyField(ProductMove, related_name='product_move_purchase_orders')
    
    request_person = models.ForeignKey(Staff, related_name='request_purchase_orders', 
            on_delete=models.PROTECT)

    approve_person = models.ForeignKey(Staff, related_name='approve_purchase_orders', 
            on_delete=models.PROTECT)

    request_date = models.DateTimeField(blank=True, null=True)
    approve_date = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    receive_date = models.DateTimeField(blank=True, null=True)

    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='invoice_purchase_order')
    note = models.CharField(max_length=500)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
                    default=OrderStatus.DRAFT.name,
                    max_length=50)