# Generated by Django 3.2.10 on 2022-07-01 09:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stats',
            name='dayInGame',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='lastUpdate',
        ),
        migrations.AddField(
            model_name='stats',
            name='bonusDragon',
            field=models.IntegerField(default=0, verbose_name='Ниндзя'),
        ),
        migrations.AddField(
            model_name='stats',
            name='bonusNinja',
            field=models.IntegerField(default=0, verbose_name='Ниндзя'),
        ),
        migrations.AddField(
            model_name='stats',
            name='byAerialBomb',
            field=models.IntegerField(default=0, verbose_name='Умер от воздушных бомб'),
        ),
        migrations.AddField(
            model_name='stats',
            name='byCar',
            field=models.IntegerField(default=0, verbose_name='Умер от машин'),
        ),
        migrations.AddField(
            model_name='stats',
            name='byGroundBomb',
            field=models.IntegerField(default=0, verbose_name='Умер от наземных бомб'),
        ),
        migrations.AddField(
            model_name='stats',
            name='byHelicopter',
            field=models.IntegerField(default=0, verbose_name='Умер от вертолетов'),
        ),
        migrations.AddField(
            model_name='stats',
            name='byHole',
            field=models.IntegerField(default=0, verbose_name='Умер от ям'),
        ),
        migrations.AddField(
            model_name='stats',
            name='byScrolling',
            field=models.IntegerField(default=0, verbose_name='Умер от пролистывания'),
        ),
        migrations.AddField(
            model_name='stats',
            name='finishedGame',
            field=models.IntegerField(default=0, verbose_name='Оконченных игр'),
        ),
        migrations.AddField(
            model_name='stats',
            name='mostTotalCharacters',
            field=models.IntegerField(default=0, verbose_name='Самая большая толпа'),
        ),
        migrations.AddField(
            model_name='stats',
            name='mostTotalCountMoney',
            field=models.IntegerField(default=0, verbose_name='Самое большое колличество собранных монет за игру'),
        ),
        migrations.AddField(
            model_name='stats',
            name='mostTotalCountMoneyInGame',
            field=models.IntegerField(default=0, verbose_name='Самое большое колличество собранных монет за игру'),
        ),
        migrations.AddField(
            model_name='stats',
            name='pedestriansEaten',
            field=models.IntegerField(default=0, verbose_name='Съедено прохожих'),
        ),
        migrations.AddField(
            model_name='stats',
            name='takedMoney',
            field=models.IntegerField(default=0, verbose_name='Собранно монет'),
        ),
        migrations.AddField(
            model_name='stats',
            name='timeSpent',
            field=models.IntegerField(default=0, verbose_name='Проведено времени'),
        ),
        migrations.AddField(
            model_name='stats',
            name='totalKilometers',
            field=models.FloatField(default=0, verbose_name='Пройдено киллометров'),
        ),
        migrations.AlterField(
            model_name='item',
            name='endurance',
            field=models.IntegerField(default=0, verbose_name='Прочность'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='uuid',
            field=models.UUIDField(auto_created=True, default=uuid.UUID('3976d8b9-bbb5-48da-b4a0-1877f2a9abdb'), primary_key=True, serialize=False, verbose_name='UUID транзации'),
        ),
    ]
