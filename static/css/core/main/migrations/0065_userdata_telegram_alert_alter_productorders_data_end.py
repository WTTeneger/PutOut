# Generated by Django 4.0.4 on 2022-06-18 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_alter_productorders_data_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='telegram_alert',
            field=models.BooleanField(default=True, verbose_name='Уведомление в тг'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 18, 13, 40, 20, 288549), verbose_name='Дата завершения'),
        ),
    ]
