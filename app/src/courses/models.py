from django.db import models
from martor.models import MartorField


class Course(models.Model):

    title = models.CharField('Название курса', max_length=130)
    description = models.TextField('Описание курса', null=True, blank=True, max_length=1200)
    cost = models.DecimalField('Стоимость курса', max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class CourseBlock(models.Model):

    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    title = models.CharField('Название учебного блока', max_length=130)
    description = models.TextField('Описание учебного блока', null=True, blank=True, max_length=1200)

    class Meta:
        verbose_name = 'Учебный блок'
        verbose_name_plural = 'Учебные блоки'


class CourseBlockLesson(models.Model):

    course_block = models.ForeignKey(CourseBlock, on_delete=models.PROTECT)
    title = models.CharField('Название урока', max_length=130)
    description = MartorField('Описание урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
