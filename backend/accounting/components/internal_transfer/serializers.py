from datetime import datetime

from rest_framework.serializers import(
    ModelSerializer, 
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    SerializerMethodField
)

from accounting.models import Account, InternalTransfer, InternalTransferItem, BankAccount, Ledger, LedgerItem
from accounting.constants import BusinessType
from core.constants import BaseStatus

class InternalTransferItemSerializer(ModelSerializer):
    class Meta:
        model = InternalTransferItem
        fields = ['transfer', 'credit_account', 'credit_account_obj', 'debit_account', 'debit_account_obj', 'note', 'amount']

    transfer = PrimaryKeyRelatedField(required=False, 
        queryset=InternalTransfer.objects.all()
    )
    
    credit_account = PrimaryKeyRelatedField(source='ledger_item.credit_account', 
        queryset=Account.objects.all()
    )

    credit_account_obj = SerializerMethodField()

    debit_account = PrimaryKeyRelatedField(source='ledger_item.debit_account', 
        queryset=Account.objects.all()
    )

    debit_account_obj = SerializerMethodField()

    amount = IntegerField(source='ledger_item.amount')
    note = CharField(required=False, source='ledger_item.note')

    def get_credit_account_obj(self, obj):
        if obj and obj.ledger_item and obj.ledger_item.credit_account:
            credit_account = obj.ledger_item.credit_account
            return {
                'id': credit_account.id,
                'code': credit_account.code,
                'name': credit_account.name,
            }

    def get_debit_account_obj(self, obj):
        if obj and obj.ledger_item and obj.ledger_item.debit_account:
            debit_account = obj.ledger_item.debit_account
            return {
                'id': debit_account.id,
                'code': debit_account.code,
                'name': debit_account.name,
            }

class InternalTransferSerializer(ModelSerializer):
    class Meta:
        model = InternalTransfer
        fields = [
                'id', 'date', 
                'from_bank_account', 'from_bank_account_obj',
                'to_bank_account', 'to_bank_account_obj',
                'note', 'amount', 'items'
            ]

    date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M:%S')
    
    from_bank_account = PrimaryKeyRelatedField(
        source='ledger.from_bank_account', 
        queryset=BankAccount.objects.all()
    )

    from_bank_account_obj = SerializerMethodField()

    to_bank_account = PrimaryKeyRelatedField(
        source='ledger.to_bank_account', 
        queryset=BankAccount.objects.all()
    )

    to_bank_account_obj = SerializerMethodField()
    
    note = CharField(source='ledger.memo')
    amount = CharField(source='ledger.amount', required=False)
    items = InternalTransferItemSerializer(many=True, required=False)

    def get_from_bank_account_obj(self, obj):
        if obj and obj.ledger and obj.ledger.from_bank_account:
            from_bank_account = obj.ledger.from_bank_account
            fields = ['id', 'name', 'account_number', 'account_holder']
            return {field: getattr(from_bank_account, field) 
                        for field in fields}

    def get_to_bank_account_obj(self, obj):
        if obj and obj.ledger and obj.ledger.to_bank_account:
            to_bank_account = obj.ledger.to_bank_account
            fields = ['id', 'name', 'account_number', 'account_holder']
            return {field: getattr(to_bank_account, field) 
                        for field in fields}

    def create_item(self, transfer, validated_item_data):
        ledger_item_data = validated_item_data.pop('ledger_item', {})
        
        ledger_item = LedgerItem.objects.create(
            ledger=transfer.ledger,
            **ledger_item_data
        )

        validated_item_data['transfer'] = transfer

        transfer_item = InternalTransferItem.objects.create(
            ledger_item=ledger_item,
            **validated_item_data
        )

        ledger_item.ref_pk = transfer_item.pk
        ledger_item.ref_class = 'accounting.InternalTransferItem'
        ledger_item.save()

        return transfer_item

    def create(self, validated_data):
        company = self.context['user'].employee.company
        date = datetime.now()

        ledger_data = validated_data.pop('ledger', {})
        items_data = validated_data.pop('items', [])

        ledger_data['cash'] = True
        ledger_data['amount'] = sum([item_data.get('ledger_item', {}).get('amount', 0) 
                                for item_data in items_data])

        ledger = Ledger.objects.create(
            company=company,
            business_type=BusinessType.INTERNAL_TRANSFER.name,
            internal=True,
            date=date,
            **ledger_data,
        )

        transfer = InternalTransfer.objects.create(
            company=company,
            ledger=ledger,
            date=date,
            status=BaseStatus.DRAFT.name
        )

        ledger.ref_class = 'accounting.InternalTransfer'
        ledger.ref_pk = transfer.pk
        ledger.save()

        for item_data in items_data:
            self.create_item(transfer, item_data)

        return transfer

    def update(self, instance, validated_data):
        ledger_data = validated_data.pop('ledger', {})
        items_data = validated_data.pop('items', [])
        
        ledger_data['amount'] = sum([item_data.get('ledger_item', {}).get('amount', 0) 
                                for item_data in items_data])

        for k,v in ledger_data.items():
            setattr(instance.ledger, k, v)

        instance.ledger.save()

        for item in instance.items.all():
            item.delete()

        for item_data in items_data:
            self.create_item(instance, item_data)

        return instance