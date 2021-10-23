# Generated by Django 3.2 on 2021-10-22 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.team'),
        ),
    ]
