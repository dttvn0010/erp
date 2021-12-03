from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from stock.models import Location, Export, ExportItem, Product, ProductMove, ProductQuantity
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
            'id', 'export_number',  'date', 'note', 'items'
        ]

    date = DateTimeField(format='%d/%m/%Y', input_formats=['%d/%m/%Y'])

    note = CharField()
    items = ExportItemSerializer(many=True, required=False)

    def create_item(self, _export, validated_item_data):
        product_move_data = validated_item_data.pop('product_move', {})
        
        product_move = ProductMove.objects.create(
            **product_move_data,
            inward=False,
            date=_export.date
        )

        cur_product_quantity = ProductQuantity.objects.filter(
            product=product_move.product,
            location=product_move.location,
            is_latest=True
        ).first()

        cur_qty = cur_product_quantity.qty if cur_product_quantity else 0

        ProductQuantity.objects.create(
            product=product_move.product,
            location=product_move.location,
            qty=cur_qty - product_move.qty,
            ref_product_move=product_move,
            is_latest=True
        )

        if cur_product_quantity is not None:
            cur_product_quantity.is_latest = False
            cur_product_quantity.save()

        validated_item_data['_export'] = _export

        return ExportItem.objects.create(
            product_move=product_move,
            **validated_item_data
        )
        
    def create(self, validated_data):
        company = self.context['user'].employee.company
        
        items_data = validated_data.pop('items', [])

        _export = Export.objects.create(
            **validated_data,
            company=company,
            status=BaseStatus.ACTIVE.name
        )

        for item_data in items_data:
            self.create_item(_export, item_data)

        return _export

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        instance.export_number = validated_data['export_number']
        instance.date = validated_data['date']
        instance.note = validated_data.get('note', '')
        instance.save()

        for item in instance.items.all():
            item.delete()

        for item_data in items_data:
            self.create_item(instance, item_data)

        return instance