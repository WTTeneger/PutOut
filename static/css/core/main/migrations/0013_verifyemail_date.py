# Generated by Django 3.2.13 on 2022-05-17 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_verifyemail_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifyemail',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
