# Generated by Django 3.2 on 2021-11-23 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_orderexpense_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_order',
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
