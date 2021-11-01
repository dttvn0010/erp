from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from manufacturing.models import Product, ProductBom, ProductBomItem
from core.constants import BaseStatus

class ProductBomItemSerializer(ModelSerializer):
    class Meta:
        model = ProductBomItem
        fields = ['bom', 'component', 'component_obj', 'qty', 'sequence']

    bom = PrimaryKeyRelatedField(required=False, 
        queryset=ProductBom.objects.all()
    )
    
    sequence = IntegerField(required=False)
    component_obj = SerializerMethodField()

    def get_component_obj(self, obj):
        if obj and obj.component:
            return {
                'id': obj.component.id,
                'name': obj.component.name,
            }

class ProductBomSerializer(ModelSerializer):
    class Meta:
        model = ProductBom
        fields = [
            'id', 'product', 'product_obj', 'name', 'status', 'items'
        ]

    product_obj = SerializerMethodField()
    status = CharField(read_only=True)
    items = ProductBomItemSerializer(many=True, required=False)

    def get_product_obj(self, obj):
        if obj and obj.product:
            return {
                'id': obj.product.id,
                'name': obj.product.name,
            }

    def create_item(self, bom, validated_item_data):
        
        validated_item_data['bom'] = bom

        return ProductBomItem.objects.create(
            **validated_item_data
        )
        
    def create(self, validated_data):

        items_data = validated_data.pop('items', [])

        bom = ProductBom.objects.create(
            **validated_data,
            status=BaseStatus.DRAFT.name
        )

        for i, item_data in enumerate(items_data):
            item_data['sequence'] = i + 1
            self.create_item(bom, item_data)

        return bom

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        instance.name = validated_data['name']
        instance.product = validated_data['product']
        instance.save()

        for item in instance.items.all():
            item.delete()

        for i,item_data in enumerate(items_data):
            item_data['sequence'] = i + 1
            self.create_item(instance, item_data)

        return instance