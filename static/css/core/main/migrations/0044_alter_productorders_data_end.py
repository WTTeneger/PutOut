# Generated by Django 4.0.4 on 2022-05-28 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_merge_20220528_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 13, 16, 51, 694672), verbose_name='Дата завершения'),
        ),
    ]
