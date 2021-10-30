from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from stock.models import Location, Import, ImportItem, Product, ProductMove
from core.constants import BaseStatus

class ImportItemSerializer(ModelSerializer):
    class Meta:
        model = ImportItem
        fields = ['_import', 'location_dest', 'location_dest_obj', 'note', 'product', 'product_obj', 'qty']

    _import = PrimaryKeyRelatedField(required=False, 
        queryset=Import.objects.all()
    )
    
    location_dest = PrimaryKeyRelatedField(source='product_move.location_dest', 
        queryset=Location.objects.all()
    )
    
    location_dest_obj = SerializerMethodField()

    product = PrimaryKeyRelatedField(source='product_move.product', 
        queryset=Product.objects.all()
    )

    product_obj = SerializerMethodField()

    qty = IntegerField(source='product_move.qty')
    note = CharField(required=False, source='product_move.note')
    
    def get_location_dest_obj(self, obj):
        if obj and obj.product_move and obj.product_move.location_dest:
            location_dest = obj.product_move.location_dest
            return {
                'id': location_dest.id,
                'name': location_dest.name,
            }

    def get_product_obj(self, obj):
        if obj and obj.product_move and obj.product_move.product:
            product = obj.product_move.product
            return {
                'id': product.id,
                'name': product.name,
            }

class ImportSerializer(ModelSerializer):
    class Meta:
        model = Import
        fields = [
            'id', 'date', 'note', 'items'
        ]

    date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M:%S')

    note = CharField()
    items = ImportItemSerializer(many=True, required=False)

    def create_item(self, _import, validated_item_data):
        product_move_data = validated_item_data.pop('product_move', {})
        
        date = datetime.now()

        product_move = ProductMove.objects.create(
            **product_move_data,
            inward=True,
            date=date
        )

        validated_item_data['_import'] = _import

        return ImportItem.objects.create(
            product_move=product_move,
            **validated_item_data
        )
        
    def create(self, validated_data):
        company = self.context['user'].employee.company
        date = datetime.now()

        items_data = validated_data.pop('items', [])

        _import = Import.objects.create(
            **validated_data,
            company=company,
            date=date,
            status=BaseStatus.DRAFT.name
        )

        for item_data in items_data:
            self.create_item(_import, item_data)

        return _import

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        instance.note = validated_data['note']
        instance.save()

        for item in instance.items.all():
            item.delete()

        for item_data in items_data:
            self.create_item(instance, item_data)

        return instance