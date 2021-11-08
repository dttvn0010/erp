# Generated by Django 3.2 on 2021-11-01 15:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('manufacturing', '0007_auto_20211101_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='company',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devicemaintainance',
            name='planned_end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 1, 15, 47, 31, 458670)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devicemaintainance',
            name='planned_start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 1, 15, 47, 36, 609307)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='devicemaintainance',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicemaintainance',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicemaintainance',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Mới tạo'), ('PLANNED', 'Đã lên kế hoạch'), ('IN_PROGRESS', 'Đang thực hiện'), ('DONE', 'Đã xong'), ('CANCELED', 'Đã hủy')], default='DRAFT', max_length=50),
        ),
    ]