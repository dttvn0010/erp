# Generated by Django 3.2 on 2021-11-01 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0004_auto_20211101_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicecategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufacturing.devicecategory'),
        ),
    ]
