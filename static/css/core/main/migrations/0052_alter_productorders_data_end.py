# Generated by Django 4.0.4 on 2022-06-04 03:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 29, 21, 879219), verbose_name='Дата завершения'),
        ),
    ]
