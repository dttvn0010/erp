from django.db import models
from django.utils.translation import gettext as _
from accounting.models import Invoice, Ledger, LedgerItem, ExpenseType
from core.models import Company, Partner, User
from stock.models import Import, Export, Product, ProductMove
from .constants import OrderStatus, OrderType

class Order(models.Model):
    company = models.ForeignKey(Company, 
        on_delete=models.PROTECT, 
        related_name='company_pu_orders'
    )

    order_number = models.CharField(max_length=100)

    type = models.CharField(choices=OrderType.choices(), max_length=50)

    ref_order = models.ForeignKey('Order', 
        blank=True, null=True, 
        on_delete=models.PROTECT
    )

    supplier = models.ForeignKey(Partner, 
        on_delete=models.PROTECT, 
        related_name='supplier_pu_orders'
    )

    ledger = models.OneToOneField(Ledger, 
        related_name='ledger_pu_order',
        on_delete=models.CASCADE
    )

    expense = models.IntegerField()
    amount_untaxed = models.IntegerField()
    amount_tax = models.IntegerField()
    amount = models.IntegerField()
    
    invoice = models.OneToOneField(Invoice,
        related_name='invoice_pu_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    _import = models.OneToOneField(Import,
        related_name='import_pu_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    _export = models.OneToOneField(Export,
        related_name='export_pu_order',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    note = models.CharField(max_length=500, blank=True)

    request_person = models.ForeignKey(User, related_name='request_pu_orders', 
            blank=True, null=True,
            on_delete=models.PROTECT)

    approve_person = models.ForeignKey(User, related_name='approve_pu_orders', 
            blank=True, null=True,
            on_delete=models.PROTECT)

    request_date = models.DateTimeField(blank=True, null=True)
    approve_date = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    receive_date = models.DateTimeField(blank=True, null=True)
    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=OrderStatus.choices(), 
        default=OrderStatus.DRAFT.name,
        max_length=50
    )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, 
        related_name='product_pu_order_items',
        on_delete=models.PROTECT
    )

    qty = models.IntegerField()
    price_unit = models.IntegerField()
    discount = models.IntegerField()
    amount_tax = models.IntegerField()
            
    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_pu_order_item',
        on_delete=models.PROTECT
    )

    product_move = models.OneToOneField(ProductMove,
        blank=True, null=True,
        related_name='product_move_pu_order_item',
        on_delete=models.PROTECT
    )

    @property
    def amount_untaxed(self):
        return self.qty * self.price_unit - self.discount

class OrderItemTax(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
        
    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_pu_order_item_tax',
        on_delete=models.PROTECT
    )

class OrderExpense(models.Model):
    order = models.ForeignKey(Order, related_name='expenses', on_delete=models.CASCADE)
    
    type = models.ForeignKey(ExpenseType, 
        related_name='expense_type_pu_order_expenses',
        on_delete=models.PROTECT
    )

    note = models.CharField(max_length=500, blank=True)

    ledger_item = models.OneToOneField(LedgerItem,
        related_name='ledger_pu_order_expense',
        on_delete=models.PROTECT
    )
