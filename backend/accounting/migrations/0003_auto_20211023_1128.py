# Generated by Django 3.2 on 2021-10-23 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('accounting', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='swift_code',
        ),
        migrations.RemoveField(
            model_name='expensetype',
            name='code',
        ),
        migrations.RemoveField(
            model_name='incometype',
            name='code',
        ),
        migrations.AddField(
            model_name='bank',
            name='code',
            field=models.CharField(default='', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bank',
            name='company',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bank',
            name='logo',
            field=models.ImageField(default='', upload_to='static/images/bank-logos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='account_holder',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
