# Generated by Django 3.2 on 2021-11-01 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0011_auto_20211101_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbomitem',
            name='bom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='manufacturing.productbom'),
        ),
    ]