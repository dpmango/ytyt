from django.db import models

from courses.models import LessonFragment
from courses_access.common.models import AccessManagerBase, AccessBase
from crm.logger import logger


class LessonFragmentAccessManager(AccessManagerBase):
    """
    Базовый менеджер для работы с доступами к фрагментам урока
    """

    def set_trial(self, lesson_fragment: LessonFragment, **kwargs):
        self.set_access(lesson_fragment=lesson_fragment, **kwargs)

    def check_permission(self, lesson_fragment_id, user, **kwargs) -> bool:
        """
        Проверка доступа к фрагменту урока.
        Метод отличается сигнатурой от базового метода и требует объекты курса и темы
        Обязательные условия предоставления доступа:
            1. У юзера отсутствует блокировка к курсу
            2. У юзера нет явной блокировки к выбранному фрагменту
        Общие условия предоставления курса:
            1. Пользователь имеет нужный доступ к фрагменту в связи с прохождением предыдущей темы (status)
            2. Пользователь оплатил доступ к курсу
        Примечание:
            - Если выбранная тема бесплатная, то доступ предоставляется без проверки оплаты в общем порядке
        :param lesson_fragment_id:
        :param user:
        :param kwargs:
        :return:
        """
        lesson_fragment_access = self.filter(lesson_fragment_id=lesson_fragment_id, user=user)
        lesson_fragment_access = lesson_fragment_access.select_related('lesson_fragment').first()

        if not lesson_fragment_access:
            return False

        if lesson_fragment_access.status == AccessBase.COURSES_STATUS_BLOCK:
            return False

        course_theme = kwargs.get('course_theme')
        if course_theme and course_theme.free_access:
            return bool(lesson_fragment_access.status in AccessBase.AVAILABLE_STATUSES)

        course = kwargs.get('course')
        course_access = course.courseaccess_set.filter(user=user).first()

        return bool(
            lesson_fragment_access.status in AccessBase.AVAILABLE_STATUSES and
            course_access.access_type in AccessBase.AVAILABLE_ACCESS_TYPES_FULL
        )


class LessonFragmentAccess(AccessBase):
    lesson_fragment = models.ForeignKey(LessonFragment, on_delete=models.CASCADE)
    objects = LessonFragmentAccessManager()

    class Meta(AccessBase.Meta):
        verbose_name = 'Доступ к фрагменту урока'
        verbose_name_plural = 'Доступ к фрагментам урока'
