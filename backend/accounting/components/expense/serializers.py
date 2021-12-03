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

from accounting.models import (
    Expense, 
    ExpenseItem, 
    ExpenseType, 
    Account, 
    BankAccount, 
    Ledger, 
    LedgerItem
)

from accounting.constants import BusinessType, ExpenseStatus

class ExpenseItemSerializer(ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = ['expense', 'type', 'type_obj', 'credit_account', 'credit_account_obj', 
                    'note', 'amount']

    expense = PrimaryKeyRelatedField(required=False, 
        queryset=Expense.objects.all()
    )
    
    credit_account = PrimaryKeyRelatedField(source='ledger_item.credit_account', 
        queryset=Account.objects.all()
    )

    amount = IntegerField(source='ledger_item.amount')
    note = CharField(required=False, source='ledger_item.note')
    type = PrimaryKeyRelatedField(queryset=ExpenseType.objects.all())
    type_obj = SerializerMethodField()
    credit_account_obj = SerializerMethodField()

    def get_type_obj(self, obj):
        if obj and obj.type:
            return {
                'id': obj.type.id,
                'name': obj.type.name
            }

    def get_credit_account_obj(self, obj):
        if obj and obj.ledger_item and obj.ledger_item.credit_account:
            credit_account = obj.ledger_item.credit_account
            return {
                'id': credit_account.id,
                'code': credit_account.code,
                'name': credit_account.name,
            }

class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = [
                'id', 'date', 
                'from_bank_account', 'from_bank_account_obj',
                'to_bank_account', 'to_bank_account_obj',
                'note', 'amount', 'cash', 'items'
            ]

    date = DateTimeField(read_only=True, source='approve_date', format='%d/%m/%Y %H:%M')
    
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
    items = ExpenseItemSerializer(many=True, required=False)

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

    def create_item(self, expense, validated_item_data):
        ledger_item_data = validated_item_data.pop('ledger_item', {})
        
        ledger_item = LedgerItem.objects.create(
            ledger=expense.ledger,
            **ledger_item_data
        )

        validated_item_data['expense'] = expense

        expense_item = ExpenseItem.objects.create(
            ledger_item=ledger_item,
            **validated_item_data
        )

        ledger_item.ref_pk = expense_item.pk
        ledger_item.ref_class = 'accounting.ExpenseItem'
        ledger_item.save()

        return expense_item

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
            business_type=BusinessType.EXPENSE.name,
            inward=False,
            date=date,
            **ledger_data
        )

        expense = Expense.objects.create(
            company=company,
            ledger=ledger,
            approve_date=date,
            status=ExpenseStatus.APPROVED.name
        )

        ledger.ref_class = 'accounting.Expense'
        ledger.ref_pk = expense.pk
        ledger.save()

        for item_data in items_data:
            self.create_item(expense, item_data)

        return expense

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