# Generated by Django 4.0.4 on 2022-05-24 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_productorders_pnl_alter_productorders_roe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikeys',
            name='title',
            field=models.CharField(default='', max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('ru', 'Russian'), ('fr', 'French'), ('uk', 'Ukraine')], default='en-us', max_length=10),
        ),
    ]
