# Generated by Django 4.0.4 on 2022-06-21 04:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0069_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pools',
            name='max_total',
            field=models.CharField(default=0, max_length=25, verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='pools',
            name='now_total',
            field=models.CharField(default=0, max_length=25, verbose_name='сумма сейчас'),
        ),
        migrations.AlterField(
            model_name='poolusers',
            name='percent',
            field=models.FloatField(default=0, verbose_name='Процент вклада'),
        ),
        migrations.AlterField(
            model_name='poolusers',
            name='total',
            field=models.FloatField(default=0, verbose_name='Сумма вклада'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 7, 33, 27, 477556), verbose_name='Дата завершения'),
        ),
    ]
