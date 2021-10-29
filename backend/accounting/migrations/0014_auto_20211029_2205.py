# Generated by Django 3.2 on 2021-10-29 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0013_auto_20211027_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseitem',
            name='expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='accounting.expense'),
        ),
        migrations.AlterField(
            model_name='incomeitem',
            name='income',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='accounting.income'),
        ),
        migrations.AlterField(
            model_name='internaltransferitem',
            name='transfer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='accounting.internaltransfer'),
        ),
    ]
