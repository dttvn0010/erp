# Generated by Django 3.2 on 2021-12-03 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20211203_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='exchange_number',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exchange',
            name='note',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='export',
            name='note',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='import',
            name='note',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='productquantity',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]