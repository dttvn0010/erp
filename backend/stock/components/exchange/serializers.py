from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from stock.models import Location, Exchange, ExchangeItem, Product, ProductMove
from core.constants import BaseStatus

class ExchangeItemSerializer(ModelSerializer):
    class Meta:
        model = ExchangeItem
        fields = ['exchange', 'location', 'location_obj', 'note', 'product', 'product_obj', 'qty']

    exchange = PrimaryKeyRelatedField(required=False, 
        queryset=Exchange.objects.all()
    )
    
    location = PrimaryKeyRelatedField(source='product_move.location', 
        queryset=Location.objects.all()
    )
    
    location_obj = SerializerMethodField()

    location_dest = PrimaryKeyRelatedField(source='product_move.location', 
        queryset=Location.objects.all()
    )
    
    location_dest_obj = SerializerMethodField()

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

class ExchangeSerializer(ModelSerializer):
    class Meta:
        model = Exchange
        fields = [
            'id', 'date', 'note', 'items'
        ]

    date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M:%S')

    note = CharField()
    items = ExchangeItemSerializer(many=True, required=False)

    def create_item(self, exchange, validated_item_data):
        product_move_data = validated_item_data.pop('product_move', {})
        
        date = datetime.now()

        product_move = ProductMove.objects.create(
            **product_move_data,
            inward=True,
            date=date
        )

        validated_item_data['exchange'] = exchange

        return ExchangeItem.objects.create(
            product_move=product_move,
            **validated_item_data
        )
        
    def create(self, validated_data):
        company = self.context['user'].employee.company
        date = datetime.now()

        items_data = validated_data.pop('items', [])

        exchange = Exchange.objects.create(
            **validated_data,
            company=company,
            date=date,
            status=BaseStatus.DRAFT.name
        )

        for item_data in items_data:
            self.create_item(exchange, item_data)

        return exchange

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        for item in instance.items.all():
            item.delete()

        for item_data in items_data:
            self.create_item(instance, item_data)

        return instance