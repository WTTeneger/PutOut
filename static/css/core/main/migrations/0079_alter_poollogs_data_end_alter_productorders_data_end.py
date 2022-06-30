# Generated by Django 4.0.4 on 2022-06-21 05:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0078_alter_productorders_data_end_poollogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poollogs',
            name='data_end',
            field=models.DateTimeField(verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 8, 35, 53, 466830), verbose_name='Дата завершения'),
        ),
    ]
