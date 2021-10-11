# Generated by Django 3.2.7 on 2021-09-25 23:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20210925_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'inventory.status.draft'), ('PLANNED', 'inventory.status.planned'), ('DONE', 'inventory.status.done'), ('CANCELED', 'inventory.status.canceled')], default='DRAFT', max_length=50),
        ),
        migrations.AddField(
            model_name='inventory',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('INACTIVE', 'Ngừng hoạt động')], default='DRAFT', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('INACTIVE', 'Ngừng hoạt động')], default='DRAFT', max_length=50),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('INACTIVE', 'Ngừng hoạt động')], default='DRAFT', max_length=50),
        ),
    ]