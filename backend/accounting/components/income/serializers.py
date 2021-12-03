from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField, 
    DateTimeField, 
    PrimaryKeyRelatedField,
    IntegerField,
    BooleanField,
    SerializerMethodField
)

from accounting.models import Account, IncomeType, Income, IncomeItem, BankAccount, Ledger, LedgerItem
from accounting.constants import BusinessType
from core.constants import BaseStatus

class IncomeItemSerializer(ModelSerializer):
    class Meta:
        model = IncomeItem
        fields = ['income', 'type', 'type_obj', 'debit_account', 'debit_account_obj', 'note', 'amount']

    income = PrimaryKeyRelatedField(required=False, 
        queryset=Income.objects.all()
    )
    
    debit_account = PrimaryKeyRelatedField(source='ledger_item.debit_account', 
        queryset=Account.objects.all()
    )

    amount = IntegerField(source='ledger_item.amount')
    note = CharField(required=False, source='ledger_item.note')
    type = PrimaryKeyRelatedField(queryset=IncomeType.objects.all())
    type_obj = SerializerMethodField()
    debit_account_obj = SerializerMethodField()

    def get_type_obj(self, obj):
        if obj and obj.type:
            return {
                'id': obj.type.id,
                'name': obj.type.name
            }

    def get_debit_account_obj(self, obj):
        if obj and obj.ledger_item and obj.ledger_item.debit_account:
            debit_account = obj.ledger_item.debit_account
            return {
                'id': debit_account.id,
                'code': debit_account.code,
                'name': debit_account.name,
            }

class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        fields = [
                'id', 'date', 
                'from_bank_account', 'from_bank_account_obj',
                'to_bank_account', 'to_bank_account_obj',
                'note', 'amount', 'cash', 'items'
        ]

    date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M')
    
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

    note = CharField(source='ledger.memo')
    amount = CharField(source='ledger.amount', required=False)
    cash = BooleanField(source='ledger.cash', required=False)
    items = IncomeItemSerializer(many=True, required=False)

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

    def create_item(self, income, validated_item_data):
        ledger_item_data = validated_item_data.pop('ledger_item', {})
        
        ledger_item = LedgerItem.objects.create(
            ledger=income.ledger,
            **ledger_item_data
        )

        validated_item_data['income'] = income

        income_item = IncomeItem.objects.create(
            ledger_item=ledger_item,
            **validated_item_data
        )

        ledger_item.ref_pk = income_item.pk
        ledger_item.ref_class = 'accounting.IncomeItem'
        ledger_item.save()

        return income_item
        
    def create(self, validated_data):
        company = self.context['user'].employee.company
        date = datetime.now()

        ledger_data = validated_data.pop('ledger', {})
        items_data = validated_data.pop('items', [])

        ledger_data['cash'] = ledger_data.get('cash') or False
        ledger_data['amount'] = sum([item_data.get('ledger_item', {}).get('amount', 0) 
                                for item_data in items_data])


        ledger = Ledger.objects.create(
            company=company,
            business_type=BusinessType.INCOME.name,
            inward=True,
            date=date,
            **ledger_data
        )

        income = Income.objects.create(
            company=company,
            ledger=ledger,
            date=date,
            status=BaseStatus.DRAFT.name
        )

        ledger.ref_class = 'accounting.Income'
        ledger.ref_pk = income.pk
        ledger.save()

        for item_data in items_data:
            self.create_item(income, item_data)

        return income

    def update(self, instance, validated_data):
        ledger_data = validated_data.pop('ledger', {})
        items_data = validated_data.pop('items', [])

        ledger_data['cash'] = ledger_data.get('cash') or False
        
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