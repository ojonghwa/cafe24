# Generated by Django 3.2.6 on 2021-09-01 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esp8266',
            name='humi',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='esp8266',
            name='temp',
            field=models.CharField(max_length=6),
        ),
    ]
