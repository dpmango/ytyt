# Generated by Django 3.1.7 on 2021-06-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicts',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Описание'),
        ),
    ]