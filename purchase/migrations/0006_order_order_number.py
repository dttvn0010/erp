# Generated by Django 3.2.7 on 2021-10-01 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_auto_20211001_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
