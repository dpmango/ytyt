from datetime import timedelta

from django.db import models, transaction
from django.utils import timezone
from rest_framework import exceptions

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

    def check_learning_speed(self, user: User, course_access) -> None:
        """
        Проверка скорости прохождения тем курса:
        Условия пропуска проверки:
            - Пользователь является сотрудником сервиса
            - У пользователя пройдено 0 или 1 тема
        Условия блокирования доступа к курсу:
            - Разница между прохождением двух тем — менее одного дня

        :param user: Модель пользователя
        :param course_access: Модель доступа к курсу
        :return: None or Raise
        """
        if user.is_staff or user.is_superuser:
            return None

        course_theme_accesses = self.filter(user=user, status=AccessBase.COURSES_STATUS_COMPLETED)
        course_theme_accesses = course_theme_accesses.select_related('course_theme').order_by('-date_completed')[:2]

        if len(course_theme_accesses) in (0, 1):
            return None

        course_theme_access_last, course_theme_access_prev = course_theme_accesses
        now = timezone.now()

        # Дополнительно проставляем даты окончания последних тем, если их не проставили ранее
        if not course_theme_access_last.date_completed:
            course_theme_access_last.date_completed = now
            course_theme_access_last.save(update_fields=['status'])

        if not course_theme_access_prev.date_completed:
            course_theme_access_prev.date_completed = now - timedelta(days=1, hours=1)
            course_theme_access_last.save(update_fields=['status'])

        delta = course_theme_access_last.date_completed - course_theme_access_prev.date_completed

        if delta > timedelta(days=1):
            return None

        course_access.status = AccessBase.COURSES_STATUS_BLOCK
        course_access.block_reason = AccessBase.BLOCK_REASON_FAST_PASSAGE
        course_access.save(update_fields=['status', 'block_reason'])

        raise exceptions.PermissionDenied({
            'detail': 'Доступ к курсу временно ограничен. Пожалуйста, свяжитесь с администрацией',
            'block_reason': dict(AccessBase.BLOCK_REASONS).get(course_access.block_reason)
        })


class CourseThemeAccess(AccessBase):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.CASCADE)
    objects = CourseThemeAccessManager()

    class Meta(AccessBase.Meta):
        verbose_name = 'Доступ к теме курса'
        verbose_name_plural = 'Доступ к темам курса'
