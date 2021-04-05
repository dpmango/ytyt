from bs4 import BeautifulSoup
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Course(models.Model):
    title = models.CharField('Название курса', max_length=1000)
    description = models.TextField('Описание курса', null=True, blank=True)
    cost = models.DecimalField('Стоимость курса', max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return '%s' % self.title


class CourseTheme(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    title = models.CharField('Название темы', max_length=1000)
    description = models.TextField('Описание темы', null=True, blank=True)
    free_access = models.BooleanField('Бесплатный доступ', default=False)

    class Meta:
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курсов'

    def __str__(self):
        return '%s' % self.title


class CourseLesson(models.Model):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.PROTECT)
    title = models.CharField('Название урока', max_length=1000)
    description = MarkdownxField('Описание урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return '%s' % self.title

    def get_description(self) -> str:
        return markdownify(self.description)

    def get_text_description(self):
        return ''.join(BeautifulSoup(self.get_description(), features='html.parser').findAll(text=True))


class LessonFragment(models.Model):
    course_lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    title = models.CharField('Название фрагмента урока', max_length=1000, null=True, blank=True)
    description = MarkdownxField('Фрагмент урока', null=True, blank=True)
    date_created = models.DateTimeField('Дата создаения фрагмента', auto_now=True)

    class Meta:
        verbose_name = 'Фрагмент урока'
        verbose_name_plural = 'Фрагменты урока'
        ordering = ('-date_created', )

    def __str__(self):
        return '%s' % self.title[:30]

    def get_description(self) -> str:
        return markdownify(self.description)  # TODO: Проверить наличие ошибки при пустом описании

    def get_text_description(self):
        return ''.join(BeautifulSoup(self.get_description(), features='html.parser').findAll(text=True))