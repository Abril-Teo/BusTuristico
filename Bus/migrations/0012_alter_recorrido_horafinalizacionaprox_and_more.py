# Generated by Django 4.2.6 on 2023-10-31 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0011_alter_atractivo_descripcion_alter_parada_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recorrido',
            name='horaFinalizacionAprox',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='recorrido',
            name='horaInicioAprox',
            field=models.TimeField(),
        ),
    ]
