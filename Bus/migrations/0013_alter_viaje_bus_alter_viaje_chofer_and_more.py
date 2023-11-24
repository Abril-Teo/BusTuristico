# Generated by Django 4.2.7 on 2023-11-10 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0012_alter_recorrido_horafinalizacionaprox_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viaje',
            name='bus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bus.bus'),
        ),
        migrations.AlterField(
            model_name='viaje',
            name='chofer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bus.chofer'),
        ),
        migrations.AlterField(
            model_name='viaje',
            name='recorrido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bus.recorrido'),
        ),
    ]
