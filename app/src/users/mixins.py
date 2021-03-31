from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


class CourseProgress(models.Model):
    """
    Модель для хранения пройденных пользователем фрагементов курса
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    passed_fragments = models.PositiveIntegerField('Количество пройденных фрагментов', default=True)


class CoursesProgressMixin(models.Model):
    """
    Миксин-класс для отслеживания прогресса курсов пользователя
    """

    user_course_progress = models.ManyToManyField(
        CourseProgress,
        verbose_name=_('Доступные курсы'),
        related_name="user_access_course_set",
        related_query_name="user_access_course",
    )

    class Meta:
        abstract = True


class CoursesAccessMixin(models.Model):
    """
    Миксин-класс для поддержки доступов к курсам
    """

    user_access_course = models.ManyToManyField(
        Course,
        verbose_name=_('Доступные курсы'),
        blank=True,
        related_name="user_access_course_set",
        related_query_name="user_access_course",
    )

    user_access_course_theme = models.ManyToManyField(
        CourseTheme,
        verbose_name=_('Доступные темы уроков'),
        blank=True,
        related_name="user_access_course_theme_set",
        related_query_name="user_access_course_theme",
    )

    user_access_course_lesson = models.ManyToManyField(
        CourseLesson,
        verbose_name=_('Доступные уроки'),
        blank=True,
        related_name="user_access_course_lesson_set",
        related_query_name="user_access_course_lesson",
    )

    class Meta:
        abstract = True
