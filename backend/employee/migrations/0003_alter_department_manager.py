# Generated by Django 3.2 on 2021-10-23 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_alter_employee_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manage_department', to='employee.employee'),
        ),
    ]