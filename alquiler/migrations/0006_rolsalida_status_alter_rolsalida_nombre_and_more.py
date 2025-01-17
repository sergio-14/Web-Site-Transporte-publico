# Generated by Django 5.0.6 on 2024-06-27 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0005_rolsalida'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolsalida',
            name='status',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('realizado', 'Realizado')], default='pendiente', max_length=10, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='rolsalida',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Agregar Turno o Descripcion'),
        ),
        migrations.AlterField(
            model_name='rolsalida',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alquiler.persona', verbose_name='Asignar Personal o Chofer'),
        ),
        migrations.AlterField(
            model_name='ventaboletos',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alquiler.persona', verbose_name='Chofer o Persona a Cargo'),
        ),
    ]
