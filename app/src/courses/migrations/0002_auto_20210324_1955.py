# Generated by Django 3.1.7 on 2021-03-24 19:55

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AlterModelOptions(
            name='courseblock',
            options={'verbose_name': 'Учебный блок', 'verbose_name_plural': 'Учебные блоки'},
        ),
        migrations.AlterModelOptions(
            name='courseblocklesson',
            options={'verbose_name': 'Урок', 'verbose_name_plural': 'Уроки'},
        ),
        migrations.AlterField(
            model_name='courseblocklesson',
            name='description',
            field=martor.models.MartorField(verbose_name='Описание урока'),
        ),
    ]