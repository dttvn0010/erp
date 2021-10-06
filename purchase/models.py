from django.db import models
from django.utils.translation import gettext as _
from accounting.models import Invoice
from core.models import Company, Partner, User
from stock.models import Location, ProductMove
from .constants import OrderStatus

# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='company_purchase_orders')

    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                        blank=True, null=True, related_name='location_purchase_orders',
                        verbose_name=_('verbose_name.purchase.order.location'))

    supplier = models.ForeignKey(Partner, on_delete=models.PROTECT,
                        verbose_name=_('verbose_name.purchase.order.supplier'))

    order_lines = models.ManyToManyField(ProductMove, related_name='product_move_purchase_orders')
    
    request_person = models.ForeignKey(User, related_name='request_purchase_orders', 
            blank=True, null=True,
            on_delete=models.PROTECT)

    approve_person = models.ForeignKey(User, related_name='approve_purchase_orders', 
            blank=True, null=True,
            on_delete=models.PROTECT)

    request_date = models.DateTimeField(blank=True, null=True)
    approve_date = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    receive_date = models.DateTimeField(blank=True, null=True)

    invoice = models.OneToOneField(Invoice, 
                blank=True, null=True,
                related_name='invoice_purchase_order',
                on_delete=models.CASCADE)

    note = models.CharField(max_length=500, verbose_name=_('verbose_name.purchase.order.note'),
                blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
                    default=OrderStatus.DRAFT.name,
                    max_length=50)