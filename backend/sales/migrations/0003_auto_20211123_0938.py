# Generated by Django 3.2 on 2021-11-23 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20211115_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='location',
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
    ]
