from rest_framework.serializers import ModelSerializer, CharField

from stock.models import ProductMove
from purchase.models import Order

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'supplier', 'note', 'supplier_name']
    
    supplier_name = CharField(read_only=True, source='supplier.name')

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = ProductMove
        fields = ['product', 'price_unit', 'qty', 'product_name']

    product_name = CharField(read_only=True, source='product.name')