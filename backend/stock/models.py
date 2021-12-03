from django.db import models
from core.models import Company
from core.constants import BaseStatus
from .constants import InventoryStatus

# Create your models here.
class ProductCategory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    parent = models.ForeignKey('ProductCategory', 
        blank=True, null=True, 
        on_delete=models.SET_NULL
    )

    code = models.CharField(max_length=100, unique=True)

    name = models.CharField(max_length=200)

    description = models.CharField(max_length=500, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    code = models.CharField(max_length=100, unique=True)

    name = models.CharField(max_length=200)

    description = models.CharField(max_length=500, blank=True)

    list_price = models.IntegerField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProductPricePolicy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    min_qty = models.IntegerField()
    max_qty = models.IntegerField()
    discount_pctg = models.FloatField()
    price = models.IntegerField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(blank=True, null=True)

class Location(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    posx = models.FloatField(blank=True, null=True)
    posy = models.FloatField(blank=True, null=True)
    posz = models.FloatField(blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class ProductMove(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    
    inward = models.BooleanField()
    internal = models.BooleanField(default=False)

    location = models.ForeignKey(Location, 
            related_name='outgoing_stock_moves', 
            on_delete=models.PROTECT,
            blank=True, null=True)

    location_dest = models.ForeignKey(Location, 
            related_name='incoming_stock_moves', 
            on_delete=models.PROTECT,
            blank=True, null=True)

    date = models.DateTimeField(blank=True, null=True)

class Import(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    import_number = models.CharField(max_length=100)
    note = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

class ImportItem(models.Model):
    _import = models.ForeignKey(Import, related_name='items', on_delete=models.CASCADE)

    product_move = models.OneToOneField(ProductMove,
        related_name='product_move_import_item',
        on_delete=models.CASCADE
    )

class Export(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    export_number = models.CharField(max_length=100)
    note = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

class ExportItem(models.Model):
    _export = models.ForeignKey(Export, related_name='items', on_delete=models.CASCADE)

    product_move = models.OneToOneField(ProductMove,
        related_name='product_move_export_item',
        on_delete=models.CASCADE
    )

class Exchange(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    exchange_number = models.CharField(max_length=100)
    note = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)    
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

class ExchangeItem(models.Model):
    exchange = models.ForeignKey(Exchange, related_name='items', on_delete=models.CASCADE)

    product_move = models.OneToOneField(ProductMove,
        related_name='product_move_exchange_item',
        on_delete=models.CASCADE
    )

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    qty = models.IntegerField()
    
    ref_product_move = models.ForeignKey(ProductMove, 
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    ref_inventory_item = models.ForeignKey('InventoryItem',
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    is_latest = models.BooleanField(default=True)

    create_date = models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=InventoryStatus.choices(), 
                default=InventoryStatus.DRAFT.name, max_length=50)

class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    theoretical_qty = models.IntegerField()
    inventory_date = models.DateTimeField()