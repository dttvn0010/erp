from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(ProductMove)
admin.site.register(ProductCategory)

admin.site.register(Import)
admin.site.register(ImportItem)

admin.site.register(Export)
admin.site.register(ExportItem)
