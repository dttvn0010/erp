# Generated by Django 3.2 on 2021-10-22 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('accounting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ledger',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='from_bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ledger_from_bank_accounts', to='accounting.bankaccount'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='to_bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ledger_to_bank_accounts', to='accounting.bankaccount'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.partner'),
        ),
        migrations.AddField(
            model_name='internaltransferitem',
            name='ledger_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_internal_transfer_item', to='accounting.ledgeritem'),
        ),
        migrations.AddField(
            model_name='internaltransferitem',
            name='transfer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.internaltransfer'),
        ),
        migrations.AddField(
            model_name='internaltransfer',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='internaltransfer',
            name='ledger',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_internal_transfer', to='accounting.ledger'),
        ),
        migrations.AddField(
            model_name='incometype',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='incomeitem',
            name='income',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.income'),
        ),
        migrations.AddField(
            model_name='incomeitem',
            name='ledger_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_income_item', to='accounting.ledgeritem'),
        ),
        migrations.AddField(
            model_name='incomeitem',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.incometype'),
        ),
        migrations.AddField(
            model_name='income',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='income',
            name='ledger',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_income', to='accounting.ledger'),
        ),
        migrations.AddField(
            model_name='expensetype',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='expenseitem',
            name='expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.expense'),
        ),
        migrations.AddField(
            model_name='expenseitem',
            name='ledger_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_expense_item', to='accounting.ledgeritem'),
        ),
        migrations.AddField(
            model_name='expenseitem',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.expensetype'),
        ),
        migrations.AddField(
            model_name='expense',
            name='approve_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approve_expenses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='expense',
            name='ledger',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_expense', to='accounting.ledger'),
        ),
        migrations.AddField(
            model_name='expense',
            name='request_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='request_expenses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.bank'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='accountbalancehistory',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.account'),
        ),
        migrations.AddField(
            model_name='accountbalancehistory',
            name='ref_ledger_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.ledgeritem'),
        ),
        migrations.AddField(
            model_name='account',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company'),
        ),
        migrations.AddField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.account'),
        ),
    ]
