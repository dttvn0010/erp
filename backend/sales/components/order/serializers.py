from datetime import datetime

from rest_framework.serializers import(
    ModelSerializer,
    CharField,
    DateTimeField,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    IntegerField
)

from core.models import Partner
from accounting.models import Ledger, LedgerItem, Invoice, InvoiceType,  BankAccount

from stock.models import (
    Import, 
    ImportItem,
    Export, 
    ExportItem,
    Product, 
    ProductMove,
    ProductQuantity,
    Location as StockLocation
)

from sales.models import (
    Order,
    OrderItem,
    OrderItemTax,
    OrderExpense
)

from accounting.constants import BusinessType
from sales.constants import OrderType, OrderStatus
from core.constants import BaseStatus

from core.utils.date_utils import format_date

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'product_obj', 'qty', 'price_unit', 
                    'stock_location', 'stock_location_obj',
                    'stock_location_dest', 'stock_location_dest_obj',
                    'discount', 'discount_pctg',
                    'amount_untaxed', 'amount_tax', 
                    'amount_tax_pctg', 'amount'
                ]


    order = PrimaryKeyRelatedField(required=False,
        queryset=Order.objects.all()
    )

    stock_location = PrimaryKeyRelatedField(
        required=False,
        source='product_move.location',
        queryset=StockLocation.objects.all()
    )

    stock_location_dest = PrimaryKeyRelatedField(
        required=False,
        source='product_move.location_dest',
        queryset=StockLocation.objects.all()
    )

    discount_pctg = SerializerMethodField()
    amount_untaxed = SerializerMethodField()
    amount = SerializerMethodField()
    amount_tax_pctg = SerializerMethodField()
    product_obj = SerializerMethodField()
    stock_location_obj = SerializerMethodField()
    stock_location_dest_obj = SerializerMethodField()

    def get_discount_pctg(self, obj):
        return 100*obj.discount/obj.price_unit

    def get_amount_tax_pctg(self, obj):
        return 100*obj.amount_tax/obj.price_unit

    def get_amount_untaxed(self, obj):
        return obj.qty * (obj.price_unit - obj.discount)

    def get_amount(self, obj):
        amount_untaxed = self.get_amount_untaxed(obj)
        return amount_untaxed + obj.amount_tax

    def get_product_obj(self, obj):
        if obj and obj.product:
            return {
                'id': obj.product.id,
                'name': obj.product.name,
            }

    def get_stock_location_obj(self, obj):
        if obj and obj.product_move and obj.product_move.location:
            location = obj.product_move.location
            return {
                'id': location.id,
                'name': location.name
            }

    def get_stock_location_dest_obj(self, obj):
        if obj and obj.product_move and obj.product_move.location_dest:
            location_dest = obj.product_move.location_dest
            return {
                'id': location_dest.id,
                'name': location_dest.name
            }

class OrderExpenseSerializer(ModelSerializer):
    class Meta:
        model = OrderExpense
        fields = ['order', 'type', 'type_obj', 'amount', 'note']

    order = PrimaryKeyRelatedField(required=False,
        queryset=Order.objects.all()
    )

    type_obj = SerializerMethodField()
    amount = IntegerField(source='ledger_item.amount')

    def get_type_obj(self, obj):
        if obj and obj.type:
            return {
                'id': obj.type.id,
                'name': obj.type.name
            }
    
        
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'type', 'customer', 'customer_obj', 
                  'order_date', 'accounting_date', 'note', 'status',
                  'from_bank_account', 'from_bank_account_obj',
                  'to_bank_account', 'to_bank_account_obj',
                  'import_number', 'import_date', 'import_note',
                  'export_number', 'export_date', 'export_note',
                  'invoice_type', 'invoice_number', 'invoice_date', 'invoice_note',
                  'items', 'expenses']

    status = CharField(read_only=True)
    order_date = DateTimeField(format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    
    customer_obj = SerializerMethodField()

    # Accounting
    accounting_date = DateTimeField(
        format='%d/%m/%Y', 
        input_formats=['%d/%m/%Y'],
        source='ledger.date'
    )
    
    from_bank_account = PrimaryKeyRelatedField(required=False, allow_null=True,
        source='ledger.from_bank_account', 
        queryset=BankAccount.objects.all()
    )
    
    from_bank_account_obj = SerializerMethodField()

    to_bank_account = PrimaryKeyRelatedField(required=False, allow_null=True,
        source='ledger.to_bank_account', 
        queryset=BankAccount.objects.all()
    )

    to_bank_account_obj = SerializerMethodField()

    # Import
    import_number = CharField(required=False, source='_import.import_number')
    
    import_date = DateTimeField(
        required=False,
        format='%d/%m/%Y', 
        input_formats=['%d/%m/%Y'],
        source='_import.date'
    )

    import_note = CharField(required=False, source='_import.note')

    # Export
    export_number = CharField(required=False, source='_export.export_number')
    
    export_date = DateTimeField(
        required=False,
        format='%d/%m/%Y', 
        input_formats=['%d/%m/%Y'],
        source='_export.date'
    )

    export_note = CharField(required=False, source='_export.note')

    # Invoice
    invoice_type = PrimaryKeyRelatedField(required=False, allow_null=True,
        source='invoice.invoice_type', 
        queryset=InvoiceType.objects.all()
    )

    invoice_number = CharField(required=False, source='invoice.invoice_number')
    invoice_note = CharField(required=False, source='invoice.note')
    invoice_date = DateTimeField(
        required=False,
        format='%d/%m/%Y', 
        input_formats=['%d/%m/%Y'],
        source='invoice.invoice_date'
    )

    # Items & Expenses

    items = OrderItemSerializer(many=True, required=False)
    expenses = OrderExpenseSerializer(many=True, required=False)

    def get_customer_obj(self, obj):
        if obj and obj.customer:
            return {
                'id': obj.customer.id,
                'name': obj.customer.name
            }

    def get_from_bank_account_obj(self, obj):
        if obj and obj.ledger and obj.ledger.from_bank_account:
            from_bank_account = obj.ledger.from_bank_account
            fields = ['id', 'name', 'account_number', 'account_holder']
            return {field: getattr(from_bank_account, field) for field in fields}

    def get_to_bank_account_obj(self, obj):
        if obj and obj.ledger and obj.ledger.to_bank_account:
            to_bank_account = obj.ledger.to_bank_account
            fields = ['id', 'name', 'account_number', 'account_holder']
            return {field: getattr(to_bank_account, field) for field in fields}

    def create_item(self, order, validated_item_data):
        product_move_data = validated_item_data.pop('product_move', {})
        product = validated_item_data['product']
        customer = order.customer
        qty = validated_item_data['qty']
        price_unit = validated_item_data['price_unit']
        discount = validated_item_data['discount'] or 0
        amount_tax = validated_item_data['amount_tax'] or 0
        amount_untaxed = qty * price_unit - discount
        order_date_str = format_date(order.order_date)
        
        ledger_item = LedgerItem.objects.create(
            ledger=order.ledger,
            note=f'Bán {qty} x {product} ngày {order_date_str} cho khách hàng {customer}', 
            amount=amount_untaxed
        )

        order_item = OrderItem.objects.create(
            order=order,
            ledger_item=ledger_item,
            product=product,
            qty=qty,
            price_unit=price_unit,
            discount=discount,
            amount_tax=amount_tax
        )

        ledger_item_tax = LedgerItem.objects.create(
            ledger=order.ledger,
            note=f'Thuế bán {qty} x {product} ngày {order_date_str} cho khách hàng {customer}',
            amount=amount_tax
        )
        
        order_item_tax = OrderItemTax.objects.create(
            order_item=order_item,
            ledger_item=ledger_item_tax
        )

        ledger_item_tax.ref_pk = order_item_tax.pk
        ledger_item_tax.ref_class = 'sales.OrderItemTax'
        ledger_item_tax.save()

        ledger_item.ref_pk = order_item.pk
        ledger_item.ref_class = 'sales.OrderItem'
        ledger_item.save()

        product_move = None
        location = None

        if order._import:
            product_move = ProductMove.objects.create(
                product=product,
                qty=qty,
                inward=True,
                date=order._import.date,
                **product_move_data
            )
            location = product_move.location_dest

            ImportItem.objects.create(
                _import=order._import,
                product_move=product_move
            )

            order_item.product_move = product_move
            order_item.save()
        
        if order._export:
            product_move = ProductMove.objects.create(
                product=product,
                qty=qty,
                inward=False,
                date=order._export.date,
                **product_move_data
            )
            location = product_move.location

            ExportItem.objects.create(
                _export=order._export,
                product_move=product_move
            )

            order_item.product_move = product_move
            order_item.save()

        if product_move:
            cur_product_quantity = ProductQuantity.objects.filter(
                product=product_move.product,
                location=location,
                is_latest=True
            ).first()

            cur_qty = cur_product_quantity.qty if cur_product_quantity else 0

            ProductQuantity.objects.create(
                product=product_move.product,
                location=location,
                qty=cur_qty + product_move.qty * (1 if product_move.inward else -1),
                ref_product_move=product_move,
                is_latest=True
            )

            if cur_product_quantity is not None:
                cur_product_quantity.is_latest = False
                cur_product_quantity.save()

        return order_item

    def create_expense(self, order, validated_expense_data):
        type = validated_expense_data['type']
        ledger_item_data = validated_expense_data.get('ledger_item', {})
        amount = ledger_item_data.get('amount', 0)
        note = validated_expense_data.get('note', '')
        order_date_str = format_date(order.order_date)

        ledger_item = LedgerItem.objects.create(
            ledger=order.ledger,
            amount=amount,
            note=f'Chi phí: {type} - bán hàng ngày {order_date_str} , khách hàng {order.customer}'
        )

        order_expense = OrderExpense.objects.create(
            order=order,
            type=type,
            note=note,
            ledger_item=ledger_item
        )

        ledger_item.ref_pk = order_expense.pk
        ledger_item.ref_class = 'sales.OrderExpense'
        ledger_item.save()

        return order_expense
    
    def create_import(self, order, validated_import_data):
        return Import.objects.create(
            company=order.company,
            status=BaseStatus.ACTIVE.name,
            **validated_import_data
        )

    def create_export(self, order, validated_export_data):
        return Export.objects.create(
            company=order.company,
            status=BaseStatus.ACTIVE.name,
            **validated_export_data
        )

    def create_invoice(self, order, validated_invoice_data):
        return Invoice.objects.create(
            partner=order.customer,
            partner_name=order.customer.name,
            partner_tax_number=order.customer.tax_number,
            partner_address=order.customer.address,
            **validated_invoice_data
        )

    def create(self, validated_data):
        company = self.context['user'].employee.company
        order_number = validated_data.pop('order_number')
        order_date = validated_data.pop('order_date')
        order_date_str = format_date(order_date)

        ledger_data = validated_data.pop('ledger', {})
        import_data = validated_data.pop('_import', {})
        export_data = validated_data.pop('_export', {})
        invoice_data = validated_data.pop('invoice', {})
      
        items_data = validated_data.pop('items', [])
        expenses_data = validated_data.pop('expenses', [])
        type = validated_data.pop('type')
        customer = validated_data.pop('customer')

        business_type = {
            OrderType.SALES.name: BusinessType.SALES.name,
            OrderType.DISCOUNT.name: BusinessType.SALES_DISCOUNT.name,
            OrderType.RETURN.name: BusinessType.SALES_RETURN.name
        }.get(type, '')

        type_str = OrderType.value_map().get(type, '')
        from_bank_account = ledger_data.get('from_bank_account')
        to_bank_account = ledger_data.get('to_bank_account')
        
        ledger = Ledger.objects.create(
            company=company,
            business_type=business_type,
            inward=True,
            date=ledger_data.get('date'),
            amount=0,
            from_bank_account=from_bank_account,
            to_bank_account=to_bank_account,
            cash=from_bank_account is not None,
            memo=f'{type_str} ngày {order_date_str} khách hàng {customer}'
        )

        order = Order.objects.create(
            company=company,
            order_number=order_number,
            ledger=ledger,
            type=type,
            customer=customer,
            order_date=order_date,
            note=validated_data.get('note',''),
            expense=0,
            amount_untaxed=0,
            amount_tax=0,
            amount=0,
            status=OrderStatus.CONFIRMED.name
        )

        if order.type == OrderType.SALES.name and export_data.get('export_number'):
            order._export = self.create_export(order, export_data)

        if order.type == OrderType.RETURN.name and import_data.get('import_number'):
            order._import = self.create_import(order, import_data)

        if invoice_data.get('invoice_number'):
            order.invoice = self.create_invoice(order, invoice_data)

        order_items = [self.create_item(order, item_data) for item_data in items_data]
        order_expenses = [self.create_expense(order, expense_data) for expense_data in expenses_data]

        order.amount_untaxed = sum([order_item.amount_untaxed for order_item in order_items])
        order.amount_tax = sum([order_item.amount_tax for order_item in order_items])
        order.expense = sum([order_expense.ledger_item.amount for order_expense in order_expenses])
        order.amount = order.amount_untaxed + order.amount_tax - order.expense
        order.save()

        ledger.amount = order.amount
        ledger.ref_pk = order.pk
        ledger.ref_class = 'sales.Order'
        ledger.save()

        return order
        
