from django.db import models

from courses.models import CourseTheme
from courses_access.common.models import AccessManagerBase, AccessBase
from courses_access.models.course_lesson import CourseLessonAccess


class CourseThemeAccessManager(AccessManagerBase):
    """
    Базовый менеджер для работы с доступами к темам курса
    """

    def set_trial(self, course_theme: CourseTheme, **kwargs):
        self.set_access(course_theme=course_theme, **kwargs)
        course_lesson = course_theme.courselesson_set.first()

        if course_lesson:
            CourseLessonAccess.objects.set_trial(course_lesson=course_lesson, **kwargs)


class CourseThemeAccess(AccessBase):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.CASCADE)
    objects = CourseThemeAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к теме курса'
        verbose_name_plural = 'Доступ к темам курса'
