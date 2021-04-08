from django.db import models, transaction

from courses.models import CourseTheme
from courses_access.common.models import AccessManagerBase, AccessBase
from courses_access.models.course_lesson import CourseLessonAccess
from users.models import User


class CourseThemeAccessManager(AccessManagerBase):
    """
    Базовый менеджер для работы с доступами к темам курса
    """

    def set_trial(self, course_theme: CourseTheme, **kwargs):
        self.set_access(course_theme=course_theme, **kwargs)
        course_lesson = course_theme.courselesson_set.first()

        if course_lesson:
            CourseLessonAccess.objects.set_trial(course_lesson=course_lesson, **kwargs)

    def set_access_with_lesson(self, course_theme: CourseTheme, user: User):
        with transaction.atomic():
            self.set_access(
                status=AccessBase.COURSES_STATUS_IN_PROGRESS, course_theme=course_theme, user=user
            )

            course_lesson = course_theme.courselesson_set.order_by('order').first()
            if course_lesson:
                CourseLessonAccess.objects.set_access_with_fragment(course_lesson, user)


class CourseThemeAccess(AccessBase):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.CASCADE)
    objects = CourseThemeAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к теме курса'
        verbose_name_plural = 'Доступ к темам курса'
