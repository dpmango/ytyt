# Generated by Django 3.1.7 on 2021-05-17 18:02

import courses.utils
from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselesson',
            name='ipynb_file',
            field=models.FileField(blank=True, null=True, upload_to=courses.utils.upload_path, verbose_name='Урок в формате .ipynb'),
        ),
        migrations.AlterField(
            model_name='courselesson',
            name='content',
            field=markdownx.models.MarkdownxField(blank=True, null=True, verbose_name='Содержание урока'),
        ),
    ]
