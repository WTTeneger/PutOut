# Generated by Django 4.0.4 on 2022-06-21 05:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0076_alter_pools_total_day_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='pools',
            name='rating',
            field=models.FloatField(default=10, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 8, 6, 49, 437659), verbose_name='Дата завершения'),
        ),
    ]
