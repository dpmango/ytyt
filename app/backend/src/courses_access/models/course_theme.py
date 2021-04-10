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

    def set_access_with_lesson(self, course_theme: CourseTheme, user: User) -> None:
        """
        Предоставление доступа к теме курса совместно с первым уроком и первым фрагментом
        :param course_theme: Тема курса
        :param user: User
        """
        with transaction.atomic():
            self.set_access(
                status=AccessBase.COURSES_STATUS_AVAILABLE, course_theme=course_theme, user=user
            )

            course_lesson = course_theme.courselesson_set.order_by('order').first()
            if course_lesson:
                CourseLessonAccess.objects.set_access_with_fragment(course_lesson, user)

    def check_permission(self, course_theme_id: int, user: User) -> bool:
        """
        Проверка доступа к теме курса.
        Обязательные условия предоставления доступа:
            1. У юзера отсутствует блокировка к курсу
            2. У юзера нет явной блокировки к выбранной теме
        Общие условия предоставления курса:
            1. Пользователь имеет нужный доступ к теме в связи с прохождением предыдущей темы (status)
            2. Пользователь оплатил доступ к курсу
        Примечание:
            - Если выбранная тема бесплатная, то доступ предоставляется без проверки оплаты в общем порядке
        :param course_theme_id: ID темы курса
        :param user: Пользователь
        """
        course_theme_access = self.filter(course_theme_id=course_theme_id, user=user)
        course_theme_access = course_theme_access.select_related('course_theme').first()

        if not course_theme_access:
            return False

        course_theme: CourseTheme = course_theme_access.course_theme
        if course_theme_access.status == AccessBase.COURSES_STATUS_BLOCK:
            return False

        if course_theme.free_access:
            return True

        course_access = course_theme.course.courseaccess_set.filter(user=user).first()
        return bool(
            course_theme_access.status in AccessBase.AVAILABLE_STATUSES and
            course_access.access_type in AccessBase.AVAILABLE_ACCESS_TYPES_FULL
        )


class CourseThemeAccess(AccessBase):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.CASCADE)
    objects = CourseThemeAccessManager()

    class Meta(AccessBase.Meta):
        verbose_name = 'Доступ к теме курса'
        verbose_name_plural = 'Доступ к темам курса'
