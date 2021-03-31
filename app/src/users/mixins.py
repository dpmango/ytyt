from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


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
        verbose_name=_('Доступные темы курса'),
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

    user_access_lesson_fragment = models.ManyToManyField(
        LessonFragment,
        verbose_name=_('Доступные фрагменты урока'),
        blank=True,
        related_name="user_access_lesson_fragment_set",
        related_query_name="user_access_lesson_fragment",
    )

    class Meta:
        abstract = True
