# Generated by Django 4.0.4 on 2022-06-02 15:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 18, 33, 56, 812269), verbose_name='Дата завершения'),
        ),
    ]
