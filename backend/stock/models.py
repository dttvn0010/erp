from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Company
from core.constants import BaseStatus
from .constants import InventoryStatus

# Create your models here.
class ProductCategory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    parent = models.ForeignKey('ProductCategory', blank=True, null=True, 
                on_delete=models.SET_NULL, 
                verbose_name=_("verbose_name.product.category.parent"))

    code = models.CharField(max_length=100, unique=True,
                verbose_name=_("verbose_name.product.category.code"))

    name = models.CharField(max_length=200, 
                verbose_name=_("verbose_name.product.category.name"))

    description = models.CharField(max_length=500, blank=True,
                verbose_name=_("verbose_name.product.category.description"))

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BaseStatus.choices(), default=BaseStatus.DRAFT.name, max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT,
                verbose_name=_("verbose_name.product.category"))

    code = models.CharField(max_length=100, unique=True,
                verbose_name=_("verbose_name.product.code"))

    name = models.CharField(max_length=200,
                verbose_name=_("verbose_name.product.name"))

    description = models.CharField(max_length=500, blank=True,
                verbose_name=_("verbose_name.product.description"))

    list_price = models.IntegerField(verbose_name=_("verbose_name.product.list.price"))

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
    incomming = models.BooleanField()

    location = models.ForeignKey(Location, 
            related_name='outgoing_stock_moves', 
            on_delete=models.PROTECT,
            blank=True, null=True)

    location_dest = models.ForeignKey(Location, 
            related_name='incoming_stock_moves', 
            on_delete=models.PROTECT,
            blank=True, null=True)

    date = models.DateTimeField(blank=True, null=True)

    product_price_policy = models.ForeignKey(ProductPricePolicy, 
                            on_delete=models.PROTECT,
                            blank=True, null=True)

    price_unit = models.IntegerField()
    price_untaxed = models.IntegerField()
    price_total = models.IntegerField()
    price_tax = models.IntegerField()
    discount = models.IntegerField()

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    qty = models.IntegerField()
    create_date = models.DateTimeField()

class Inventory(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    date = models.DateTimeField()

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=InventoryStatus.choices(), 
                default=InventoryStatus.DRAFT.name, max_length=50)

class InventoryLine(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    theoretical_qty = models.IntegerField()
    inventory_date = models.DateTimeField()