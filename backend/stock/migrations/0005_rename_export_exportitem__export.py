# Generated by Django 3.2 on 2021-11-30 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20211129_2215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exportitem',
            old_name='export',
            new_name='_export',
        ),
    ]