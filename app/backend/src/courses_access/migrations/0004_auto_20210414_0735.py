# Generated by Django 3.1.7 on 2021-04-14 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_access', '0003_auto_20210410_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseaccess',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AddField(
            model_name='courselessonaccess',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AddField(
            model_name='coursethemeaccess',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AddField(
            model_name='lessonfragmentaccess',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения'),
        ),
    ]