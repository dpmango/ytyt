# Generated by Django 3.1.7 on 2021-04-23 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0003_auto_20210422_1149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialogmessage',
            options={'ordering': ('date_created',)},
        ),
    ]