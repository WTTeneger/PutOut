# Generated by Django 4.0.4 on 2022-06-21 04:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 7, 35, 52, 712601), verbose_name='Дата завершения'),
        ),
    ]
