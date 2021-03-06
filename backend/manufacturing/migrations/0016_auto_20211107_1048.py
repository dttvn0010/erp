# Generated by Django 3.2 on 2021-11-07 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0015_auto_20211102_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionworkflowstep',
            name='prior_steps',
            field=models.ManyToManyField(blank=True, to='manufacturing.ProductionWorkflowStep'),
        ),
        migrations.CreateModel(
            name='ProductionStepDeviceUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manufacturing.device')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_uses', to='manufacturing.productionstep')),
            ],
        ),
    ]
