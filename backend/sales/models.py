from django.db import models
from core.models import Company, Partner
from accounting.models import Invoice
from stock.models import ProductMove
from .constants import OrderStatus
# Create your models here.

class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='company_sale_orders')
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name='partner_sale_orders')
    order_lines = models.ManyToManyField(ProductMove, related_name='product_move_sale_orders')
    date_order = models.DateTimeField()
    
    invoice = models.OneToOneField(Invoice, 
                    related_name='invoice_sale_orders',
                    blank=True, null=True,
                    on_delete=models.CASCADE)

    note = models.CharField(max_length=500)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
                    default=OrderStatus.DRAFT.name,
                    max_length=50)