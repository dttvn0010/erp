from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from stock.models import Location, Export, ExportItem, Product, ProductMove
from core.constants import BaseStatus

class ExportItemSerializer(ModelSerializer):
    class Meta:
        model = ExportItem
        fields = ['_export', 'location', 'location_obj', 'note', 'product', 'product_obj', 'qty']

    _export = PrimaryKeyRelatedField(required=False, 
        queryset=Export.objects.all()
    )
    
    location = PrimaryKeyRelatedField(source='product_move.location', 
        queryset=Location.objects.all()
    )
    
    location_obj = SerializerMethodField()

    product = PrimaryKeyRelatedField(source='product_move.product', 
        queryset=Product.objects.all()
    )

    product_obj = SerializerMethodField()

    qty = IntegerField(source='product_move.qty')
    note = CharField(required=False, source='product_move.note')
    
    def get_location_obj(self, obj):
        if obj and obj.product_move and obj.product_move.location:
            location = obj.product_move.location
            return {
                'id': location.id,
                'name': location.name,
            }

    def get_product_obj(self, obj):
        if obj and obj.product_move and obj.product_move.product:
            product = obj.product_move.product
            return {
                'id': product.id,
                'name': product.name,
            }

class ExportSerializer(ModelSerializer):
    class Meta:
        model = Export
        fields = [
            'id', 'date', 'note', 'items'
        ]

    date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M:%S')

    note = CharField()
    items = ExportItemSerializer(many=True, required=False)

    def create_item(self, _export, validated_item_data):
        product_move_data = validated_item_data.pop('product_move', {})
        
        date = datetime.now()

        product_move = ProductMove.objects.create(
            **product_move_data,
            inward=True,
            date=date
        )

        validated_item_data['_export'] = _export

        return ExportItem.objects.create(
            product_move=product_move,
            **validated_item_data
        )
        
    def create(self, validated_data):
        company = self.context['user'].employee.company
        date = datetime.now()

        items_data = validated_data.pop('items', [])

        _export = Export.objects.create(
            **validated_data,
            company=company,
            date=date,
            status=BaseStatus.DRAFT.name
        )

        for item_data in items_data:
            self.create_item(_export, item_data)

        return _export

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        instance.note = validated_data['note']
        instance.save()

        for item in instance.items.all():
            item.delete()

        for item_data in items_data:
            self.create_item(instance, item_data)

        return instance