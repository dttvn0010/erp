# Generated by Django 3.2 on 2021-10-25 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_auto_20211023_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.expensetype'),
        ),
        migrations.AddField(
            model_name='income',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.incometype'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('INACTIVE', 'Ngừng hoạt động')], default='DRAFT', max_length=50),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('INACTIVE', 'Ngừng hoạt động')], default='DRAFT', max_length=50),
        ),
    ]
