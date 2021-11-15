# Generated by Django 3.2 on 2021-11-15 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211102_1023'),
        ('accounting', '0014_auto_20211029_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='note',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.CreateModel(
            name='InvoiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.invoicetype'),
        ),
    ]