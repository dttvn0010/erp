# Generated by Django 3.2.7 on 2021-10-01 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_alter_product_properties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmove',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]