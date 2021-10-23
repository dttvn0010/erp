from django.db import models
from core.models import Company, Partner
from stock.models import Location, Export, Product, ProductPricePolicy
from accounting.models import Invoice, Ledger, LedgerItem, ExpenseType

from .constants import OrderStatus, OrderType
# Create your models here.

class Order(models.Model):
    company = models.ForeignKey(Company, 
        on_delete=models.PROTECT, 
        related_name='company_sa_orders'
    )

    type = models.CharField(choices=OrderType.choices(), max_length=50)

    ref_order = models.ForeignKey('Order', 
        blank=True, null=True, 
        on_delete=models.PROTECT
    )

    customer = models.ForeignKey(Partner, 
        on_delete=models.PROTECT, 
        related_name='customer_sa_orders'
    )
    
    location = models.ForeignKey(Location, 
        on_delete=models.PROTECT,
        related_name='location_sa_orders',
        blank=True, null=True
    )

    ledger = models.OneToOneField(Ledger, 
        related_name='ledger_sa_order',
        on_delete=models.CASCADE
    )

    discount = models.IntegerField()
    expense = models.IntegerField()
    amount_untaxed = models.IntegerField()
    amount_tax = models.IntegerField()
    amount = models.IntegerField()

    date_order = models.DateTimeField()
    
    invoice = models.OneToOneField(Invoice,
        related_name='invoice_sa_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    _export = models.OneToOneField(Export,
        related_name='export_sa_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    note = models.CharField(max_length=500)
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
        default=OrderStatus.DRAFT.name,
        max_length=50
    )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, 
        related_name='product_sa_order_items',
        on_delete=models.PROTECT
    )

    qty = models.IntegerField()
    price_unit = models.IntegerField()

    product_price_policy = models.ForeignKey(ProductPricePolicy, 
        on_delete=models.PROTECT,
        related_name='price_policy_sa_order_items',
        blank=True, null=True
    )

    discount = models.IntegerField()
    expense = models.IntegerField()
    amount_untaxed = models.IntegerField()
    amount_tax = models.IntegerField()
    amount = models.IntegerField()

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_sa_order_item',
        on_delete=models.PROTECT
    )

class OrderItemTax(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    tax_rate = models.FloatField()
    amount_tax = models.IntegerField()

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_sa_order_item_tax',
        on_delete=models.PROTECT
    )

class OrderExpense(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    type = models.ForeignKey(ExpenseType, 
        related_name='expense_type_sa_order_expenses',
        on_delete=models.PROTECT
    )

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_sa_order_expense',
        on_delete=models.PROTECT
    )
