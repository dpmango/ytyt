# Generated by Django 3.1.7 on 2021-04-13 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210413_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_notifications',
            field=models.BooleanField(default=False, verbose_name='Уведомления на почту'),
        ),
    ]