# Generated by Django 3.1.7 on 2021-06-09 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20210607_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Файл'), (2, 'Изображение')], default=1, verbose_name='Тип файла'),
        ),
    ]
