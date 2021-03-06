# Generated by Django 4.0.4 on 2022-05-21 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_client_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('symbol', models.CharField(max_length=15, verbose_name='Пара')),
                ('id_order', models.CharField(max_length=15, verbose_name='id')),
                ('status', models.CharField(max_length=20, verbose_name='Статус')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Логи',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
