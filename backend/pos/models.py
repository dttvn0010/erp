from django.db import models
from stock.models import Product
from core.models import Company, Partner
from accounting.models import  Invoice, ExpenseType, Ledger, LedgerItem
from stock.models import ProductPricePolicy, Export
from core.constants import BaseStatus
from .constants import OrderStatus, OrderType
# Create your models here.

class Location(models.Model):
    company = models.ForeignKey(Company, 
        related_name='company_pos_locations',
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), 
				default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    company = models.ForeignKey(Company, 
        on_delete=models.PROTECT, 
        related_name='company_pos_orders'
    )

    order_number = models.CharField(max_length=100)

    type = models.CharField(choices=OrderType.choices(), max_length=50)

    ref_order = models.ForeignKey('Order', 
        blank=True, null=True, 
        on_delete=models.PROTECT
    )

    customer = models.ForeignKey(Partner, 
        on_delete=models.PROTECT, 
        related_name='customer_pos_orders'
    )
    
    location = models.ForeignKey(Location, 
        on_delete=models.PROTECT,
        related_name='location_pos_orders',
        blank=True, null=True
    )

    ledger = models.OneToOneField(Ledger, 
        related_name='ledger_pos_order',
        on_delete=models.CASCADE
    )

    expense = models.IntegerField()
    amount_untaxed = models.IntegerField()
    amount_tax = models.IntegerField()
    amount = models.IntegerField()

    invoice = models.OneToOneField(Invoice,
        related_name='invoice_pos_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    _export = models.OneToOneField(Export,
        related_name='export_pos_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    note = models.CharField(max_length=500, blank=True)

    order_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
        default=OrderStatus.DRAFT.name,
        max_length=50
    )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, 
        related_name='product_pos_order_items',
        on_delete=models.PROTECT
    )

    qty = models.IntegerField()
    price_unit = models.IntegerField()

    product_price_policy = models.ForeignKey(ProductPricePolicy, 
        on_delete=models.PROTECT,
        related_name='price_policy_pos_order_items',
        blank=True, null=True
    )

    discount = models.IntegerField()
    amount_tax = models.IntegerField()

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_pos_order_item',
        on_delete=models.PROTECT
    )

class OrderItemTax(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    
    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_pos_order_item_tax',
        on_delete=models.PROTECT
    )

class OrderExpense(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    type = models.ForeignKey(ExpenseType,
        related_name='expense_type_pos_order_expenses',
        on_delete=models.PROTECT
    )

    note = models.CharField(max_length=500, blank=True)

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_pos_order_expense',
        on_delete=models.PROTECT
    )
