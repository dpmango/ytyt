# Generated by Django 3.1.7 on 2021-04-01 06:18

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_lessonfragment_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonfragment',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, null=True, verbose_name='Фрагмент урока'),
        ),
    ]
