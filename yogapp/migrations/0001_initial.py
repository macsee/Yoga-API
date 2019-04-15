# Generated by Django 2.1.1 on 2018-12-03 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=100)),
                ('dni', models.CharField(blank=True, max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=255)),
                ('ciudad', models.CharField(blank=True, max_length=255)),
                ('fecha_nac', models.DateField(blank=True, null=True)),
                ('fecha_ing', models.DateTimeField(auto_now_add=True)),
                ('tel_contacto', models.CharField(blank=True, max_length=100)),
                ('obra_social', models.CharField(blank=True, max_length=100)),
                ('antecedentes', models.TextField(blank=True, max_length=500)),
                ('membresia', models.CharField(blank=True, max_length=10)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('presente', models.BooleanField(default=False)),
                ('fecha_init', models.DateField(auto_now=True)),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('dia', models.CharField(max_length=2)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('cupo', models.IntegerField(default=0)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CuentaCorriente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('concepto', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_total', models.IntegerField(default=0)),
                ('valor_pagado', models.IntegerField(default=0)),
                ('concepto', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=100)),
                ('dni', models.CharField(blank=True, max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=255)),
                ('ciudad', models.CharField(blank=True, max_length=255)),
                ('fecha_nac', models.DateField(blank=True, null=True)),
                ('fecha_ing', models.DateTimeField(auto_now_add=True)),
                ('especialidad', models.ManyToManyField(blank=True, to='yogapp.Especialidad')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroClase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('cupo', models.IntegerField(default=0)),
                ('estado', models.CharField(blank=True, max_length=100)),
                ('clase_orig', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.Clase')),
                ('profesor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.Profesor')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='clase',
            name='profesor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.Profesor'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='clase_registro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yogapp.RegistroClase'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='clases',
            field=models.ManyToManyField(blank=True, to='yogapp.Clase'),
        ),
    ]
