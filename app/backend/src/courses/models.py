from bs4 import BeautifulSoup
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class CourseBase(models.Model):
    order = models.PositiveIntegerField('Порядок следования', default=0, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('order',)


class Course(CourseBase):
    title = models.CharField('Название курса', max_length=1000)
    description = models.TextField('Описание курса', null=True, blank=True)
    cost = models.DecimalField('Стоимость курса', max_digits=11, decimal_places=2)

    class Meta(CourseBase.Meta):
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return '%s' % self.title


class CourseTheme(CourseBase):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    title = models.CharField('Название темы', max_length=1000)
    free_access = models.BooleanField('Бесплатный доступ', default=False)

    class Meta(CourseBase.Meta):
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курсов'

    def __str__(self):
        return '%s' % self.title


class CourseLesson(CourseBase):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.PROTECT)
    title = models.CharField('Название урока', max_length=1000)
    description = models.CharField('Описание урока', max_length=1000)
    content = MarkdownxField('Содержание урока')

    class Meta(CourseBase.Meta):
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return '%s' % self.title


class LessonFragment(models.Model):
    course_lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    title = models.CharField('Название фрагмента урока', max_length=1000, null=True, blank=True)
    content = MarkdownxField('Содержание фрагмента', null=True, blank=True)
    date_created = models.DateTimeField('Дата создаения фрагмента', auto_now=True)

    class Meta:
        verbose_name = 'Фрагмент урока'
        verbose_name_plural = 'Фрагменты урока'
        ordering = ('date_created', )

    def __str__(self):
        return '%s' % self.title[:30]

    def get_content(self) -> str:
        return markdownify(self.content)  # TODO: Проверить наличие ошибки при пустом описании

    def get_text_content(self):
        return ''.join(BeautifulSoup(self.content(), features='html.parser').findAll(text=True))
