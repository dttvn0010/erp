# Generated by Django 3.2 on 2021-11-08 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0018_auto_20211108_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionstep',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='manufacturing.productionprocess'),
        ),
    ]