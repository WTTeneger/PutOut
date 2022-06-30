# Generated by Django 3.2.10 on 2022-05-15 13:40

import core.main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userdata_bonus_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='balance',
            field=models.FloatField(default=0, validators=[core.main.models.validate_decimals], verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='bonus_balance',
            field=models.FloatField(default=0, validators=[core.main.models.validate_decimals], verbose_name='Бонусный баланс'),
        ),
    ]