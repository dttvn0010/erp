# Generated by Django 3.2 on 2021-11-23 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_auto_20211115_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='amount_untaxed',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='expense',
        ),
        migrations.RemoveField(
            model_name='orderitemtax',
            name='amount_tax',
        ),
        migrations.RemoveField(
            model_name='orderitemtax',
            name='tax_rate',
        ),
        migrations.AlterField(
            model_name='orderexpense',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='purchase.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='purchase.order'),
        ),
    ]
