# Generated by Django 3.1.7 on 2021-04-05 05:20

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Название курса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание курса')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Стоимость курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='CourseLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Название урока')),
                ('description', markdownx.models.MarkdownxField(verbose_name='Описание урока')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
        migrations.CreateModel(
            name='LessonFragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Название фрагмента урока')),
                ('description', markdownx.models.MarkdownxField(blank=True, null=True, verbose_name='Фрагмент урока')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Дата создаения фрагмента')),
                ('course_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courselesson')),
            ],
            options={
                'verbose_name': 'Фрагмент урока',
                'verbose_name_plural': 'Фрагменты урока',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='CourseTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Название темы')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание темы')),
                ('free_access', models.BooleanField(default=False, verbose_name='Бесплатный доступ')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courses.course')),
            ],
            options={
                'verbose_name': 'Тема курса',
                'verbose_name_plural': 'Темы курсов',
            },
        ),
        migrations.AddField(
            model_name='courselesson',
            name='course_theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courses.coursetheme'),
        ),
    ]
