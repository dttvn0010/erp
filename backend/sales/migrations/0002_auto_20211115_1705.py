# Generated by Django 3.2 on 2021-11-15 17:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20211030_1636'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='_import',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='import_sa_order', to='stock.import'),
        ),
        migrations.AddField(
            model_name='order',
            name='accounting_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 15, 17, 5, 37, 472626)),
            preserve_default=False,
        ),
    ]
