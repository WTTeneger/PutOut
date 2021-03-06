# Generated by Django 4.0.4 on 2022-05-28 03:47

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_alter_productorders_data_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='id_order',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='to',
        ),
        migrations.AddField(
            model_name='transactions',
            name='data_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='from_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userdata', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='id ордера'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 6, 47, 24, 636331), verbose_name='Дата завершения'),
        ),
    ]
