# Generated by Django 2.1.1 on 2018-10-27 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yogapp', '0003_auto_20181027_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroclase',
            name='cupo',
            field=models.IntegerField(default=0),
        ),
    ]
