# Generated by Django 3.1.7 on 2021-04-22 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0004_auto_20210413_2249'),
        ('dialogs', '0002_dialogmessage_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogmessage',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.courselesson'),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='dialog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dialogs.dialog'),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
