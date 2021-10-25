# Generated by Django 3.2 on 2021-10-25 19:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_auto_20211025_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='internaltransferitem',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
