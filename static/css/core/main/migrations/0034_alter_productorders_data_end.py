# Generated by Django 4.0.4 on 2022-05-26 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_productorders_data_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 13, 34, 54, 556943), verbose_name='Дата завершения'),
        ),
    ]