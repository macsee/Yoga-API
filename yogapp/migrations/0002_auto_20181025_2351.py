# Generated by Django 2.1.1 on 2018-10-25 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yogapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='fecha_nac',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='fecha_nac',
            field=models.DateField(blank=True, null=True),
        ),
    ]
