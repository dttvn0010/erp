# Generated by Django 3.2 on 2021-11-23 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='amount_tax',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='amount_untaxed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='expense',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
