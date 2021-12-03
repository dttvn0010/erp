
from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from stock.models import Location, Import, ImportItem, Product, ProductMove, ProductQuantity
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
            'id', 'import_number', 'date', 'note', 'items'
        ]

    date = DateTimeField(format='%d/%m/%Y %H:%M', input_formats=['%d/%m/%Y %H:%M'])

    note = CharField(required=False)
    items = ImportItemSerializer(many=True, required=False)

    def create_item(self, _import, validated_item_data):
        product_move_data = validated_item_data.pop('product_move', {})
        product_move = ProductMove.objects.create(
            **product_move_data,
            inward=True,
            date=_import.date
        )

        cur_product_quantity = ProductQuantity.objects.filter(
            product=product_move.product,
            location=product_move.location_dest,
            is_latest=True
        ).first()

        cur_qty = cur_product_quantity.qty if cur_product_quantity else 0

        ProductQuantity.objects.create(
            product=product_move.product,
            location=product_move.location_dest,
            qty=cur_qty + product_move.qty,
            ref_product_move=product_move,
            is_latest=True
        )

        if cur_product_quantity is not None:
            cur_product_quantity.is_latest = False
            cur_product_quantity.save()

        validated_item_data['_import'] = _import

        return ImportItem.objects.create(
            product_move=product_move,
            **validated_item_data
        )
        
    def create(self, validated_data):
        company = self.context['user'].employee.company
        items_data = validated_data.pop('items', [])

        _import = Import.objects.create(
            **validated_data,
            company=company,
            status=BaseStatus.ACTIVE.name
        )

        for item_data in items_data:
            self.create_item(_import, item_data)

        return _import

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        instance.import_number = validated_data['import_number']
        instance.date = validated_data['date']
        instance.note = validated_data.get('note', '')
        instance.save()

        for item in instance.items.all():
            item.delete()

        for item_data in items_data:
            self.create_item(instance, item_data)

        return instance