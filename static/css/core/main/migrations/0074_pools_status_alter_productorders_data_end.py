# Generated by Django 4.0.4 on 2022-06-21 04:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0073_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='pools',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 7, 42, 42, 739973), verbose_name='Дата завершения'),
        ),
    ]
