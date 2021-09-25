from django.db import models
from core.models import Company, Partner
from accounting.models import Invoice
from stock.models import Location, ProductMove
from .constants import OrderStatus
# Create your models here.

class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='company_pos_orders')
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name='partner_pos_orders')
    
    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                    blank=True, null=True, related_name='location_pos_orders')

    order_lines = models.ManyToManyField(ProductMove, related_name='product_move_pos_orders')
    date_order = models.DateTimeField()
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='invoice_pos_order')
    note = models.CharField(max_length=500)
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
                default=OrderStatus.DRAFT.name,
                max_length=50)