from datetime import datetime
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, PrimaryKeyRelatedField
from accounting.models import InternalTransfer, BankAccount, Ledger
from accounting.constants import BusinessType
from core.constants import BaseStatus

class InternalTransferSerializer(ModelSerializer):
    class Meta:
        model = InternalTransfer
        fields = [
                'id', 'date', 
                'from_bank_account', 'from_bank_account_name', 'from_bank_account_number',
                'to_bank_account', 'to_bank_account_name', 'to_bank_account_number',
                'note', 'amount']

    date = DateTimeField(read_only=True, format='%d/%m/%Y %H:%M:%S')
    
    from_bank_account = PrimaryKeyRelatedField(allow_empty=True, source='ledger.from_bank_account', queryset=BankAccount.objects.all())
    from_bank_account_name = CharField(read_only=True, source='ledger.from_bank_account.name')
    from_bank_account_number = CharField(read_only=True, source='ledger.from_bank_account.account_number')

    to_bank_account = PrimaryKeyRelatedField(allow_empty=True, source='ledger.to_bank_account', queryset=BankAccount.objects.all())
    to_bank_account_name = CharField(read_only=True, source='ledger.to_bank_account.name')
    to_bank_account_number = CharField(read_only=True, source='ledger.to_bank_account.account_number')

    note = CharField(source='ledger.memo', allow_blank=True)
    amount = CharField(source='ledger.amount')

    def create(self, validated_data):
        company = self.context['user'].employee.company
        date = datetime.now()

        ledger = Ledger.objects.create(
            company=company,
            business_type=BusinessType.INTERNAL_TRANSFER.name,
            internal=True,
            date=date,
            **validated_data.get('ledger', {})
        )

        internal_transfer = InternalTransfer.objects.create(
            company=company,
            ledger=ledger,
            date=date,
            status=BaseStatus.DRAFT.name
        )

        ledger.ref_class = 'accounting.InternalTransfer'
        ledger.ref_pk = internal_transfer.pk
        ledger.save()

        return internal_transfer