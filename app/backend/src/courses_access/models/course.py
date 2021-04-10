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
        status = self.model.COURSES_STATUS_AVAILABLE
        course_access, _ = self.model.objects.get_or_create(
            access_type=self.model.COURSE_ACCESS_TYPE_TRIAL, status=status, course=course, user=user,
        )
        course_theme = course.coursetheme_set.filter(free_access=True).first()
        if course_theme:
            CourseThemeAccess.objects.set_trial(course_theme=course_theme, user=user, status=status)

    def check_permission(self, course_id, user) -> bool:
        """
        Метод проверяет наличие любого доступа к курсу
        :param course_id: ID курса для проверки
        :param user: User
        """
        course_access = self.filter(course_id=course_id, user=user).first()
        if not course_access:
            return False

        return bool(
            course_access.access_type in AccessBase.AVAILABLE_ACCESS_TYPES and
            course_access.status in AccessBase.AVAILABLE_STATUSES
        )


class CourseAccess(AccessBase):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    access_type = models.PositiveSmallIntegerField(
        'Тип доступа', choices=AccessBase.COURSE_ACCESS_TYPES, default=AccessBase.COURSE_ACCESS_TYPE_TRIAL
    )
    objects = CourseAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'
