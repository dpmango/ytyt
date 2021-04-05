# Generated by Django 3.1.7 on 2021-04-05 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses_access', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonfragmentaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursethemeaccess',
            name='course_theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursetheme'),
        ),
        migrations.AddField(
            model_name='coursethemeaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courselessonaccess',
            name='course_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courselesson'),
        ),
        migrations.AddField(
            model_name='courselessonaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseaccess',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='courseaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
