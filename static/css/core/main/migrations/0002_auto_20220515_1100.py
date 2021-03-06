# Generated by Django 3.2.10 on 2022-05-15 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='line_1',
            field=models.ManyToManyField(related_name='line_1', to='main.UserData', verbose_name='Линия 1'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='line_2',
            field=models.ManyToManyField(related_name='line_2', to='main.UserData', verbose_name='Линия 2'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='line_3',
            field=models.ManyToManyField(related_name='line_3', to='main.UserData', verbose_name='Линия 3'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.client', verbose_name='Если покупатель'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='trader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.trader', verbose_name='Если трейдер'),
        ),
    ]
