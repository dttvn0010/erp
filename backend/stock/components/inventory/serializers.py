
from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from stock.models import Location, Inventory, InventoryItem, ProductQuantity
from core.constants import BaseStatus

class InventoryItemSerializer(ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['inventory', 'product', 'product_obj', 'theoretical_qty', 'qty', 'note']

    inventory = PrimaryKeyRelatedField(required=False, 
        queryset=Inventory.objects.all()
    )
    
    product_obj = SerializerMethodField()

    def get_product_obj(self, obj):
        if obj and obj.product:
            product = obj.product
            return {
                'id': product.id,
                'name': product.name,
            }

class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'id', 'inventory_number', 'location',  'location_obj', 'date', 'note', 'items'
        ]

    date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])
    location_obj = SerializerMethodField()
    items = InventoryItemSerializer(many=True, required=False)

    def get_location_obj(self, obj):
        if obj and obj.location:
            location =  obj.location
            return {
                'id': location.id,
                'name': location.name
            }

    def create_item(self, inventory, validated_item_data):
        validated_item_data['inventory'] = inventory

        inventory_item = InventoryItem.objects.create(
            **validated_item_data
        )

        cur_product_quantity = ProductQuantity.objects.filter(
            product=inventory_item.product,
            location=inventory.location,
            is_latest=True
        ).first()

        if cur_product_quantity is not None:
            cur_product_quantity.is_latest = False
            cur_product_quantity.save()

        ProductQuantity.objects.create(
            product=inventory_item.product,
            location=inventory.location,
            qty=inventory_item.qty,
            ref_inventory_item=inventory_item,
            is_latest=True
        )

        return inventory_item
        
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        inventory = Inventory.objects.create(
            **validated_data,
            status=BaseStatus.ACTIVE.name
        )

        for item_data in items_data:
            self.create_item(inventory, item_data)

        return inventory