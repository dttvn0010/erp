# Generated by Django 3.2 on 2021-10-22 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]