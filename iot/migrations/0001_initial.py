# Generated by Django 3.2.6 on 2021-09-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Esp8266',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('espid', models.CharField(max_length=10)),
                ('temp', models.DecimalField(decimal_places=2, max_digits=3)),
                ('humi', models.DecimalField(decimal_places=2, max_digits=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
