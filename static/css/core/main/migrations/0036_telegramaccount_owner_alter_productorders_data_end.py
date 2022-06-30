# Generated by Django 4.0.4 on 2022-05-27 10:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_telegramaccount_alter_productorders_data_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramaccount',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userdata', verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 27, 13, 33, 4, 947315), verbose_name='Дата завершения'),
        ),
    ]
