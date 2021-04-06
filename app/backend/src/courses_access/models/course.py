from django.db import models

from courses.models import Course
from courses_access.common.models import AccessManagerBase, AccessBase
from courses_access.models.course_theme import CourseThemeAccess
from users.models import User


class CourseAccessManager(AccessManagerBase):
    def set_access(self) -> None:
        """
        Метод намереннно переопределен и убран, так как получить доступ к курсу просто так нельзя
        """
        pass

    def set_trial(self, course: Course, user: User) -> None:
        """
        Метод добавляет доступ к:
            - Course.first()
            - CourseTheme.first()
            - CourseLesson.first()
            - LessonFragment.first()
        Метод по очереди вызывает `set_trial` из нужного класса и предоставляет доступ для юзера
        """
        status = AccessBase.COURSES_STATUS_AVAILABLE
        course_access, _ = CourseAccess.objects.get_or_create(
            access_type=CourseAccess.COURSE_ACCESS_TYPE_TRIAL, status=status, course=course, user=user,
        )
        course_theme = course.coursetheme_set.filter(free_access=True).first()
        if course_theme:
            CourseThemeAccess.objects.set_trial(course_theme=course_theme, user=user, status=status)


class CourseAccess(AccessBase):
    COURSE_ACCESS_TYPE_TRIAL = 1
    COURSE_ACCESS_TYPE_FULL_PAID = 2  # TODO: При сохранении из админки не давать доступ к добавлению этого параметра
    COURSE_ACCESS_TYPE_FULL_UNPAID = 3

    COURSE_ACCESS_TYPES = (
        (COURSE_ACCESS_TYPE_TRIAL, 'Пробный'),
        (COURSE_ACCESS_TYPE_FULL_PAID, 'Полный оплаченный'),
        (COURSE_ACCESS_TYPE_FULL_UNPAID, 'Полный неоплаченный'),
    )

    access_type = models.PositiveSmallIntegerField(
        'Тип доступа', choices=COURSE_ACCESS_TYPES, default=COURSE_ACCESS_TYPE_TRIAL
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    objects = CourseAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'
