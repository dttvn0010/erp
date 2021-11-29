# Generated by Django 3.2 on 2021-11-23 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20211123_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[('SALES', 'sales.order.type.sale'), ('DISCOUNT', 'sales.order.type.discount'), ('RETURN', 'sales.order.type.return')], max_length=50),
        ),
    ]
