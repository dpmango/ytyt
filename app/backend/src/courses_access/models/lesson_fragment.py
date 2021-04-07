from django.db import models

from courses.models import LessonFragment
from courses_access.common.models import AccessManagerBase, AccessBase
from users.models import User


class LessonFragmentAccessManager(AccessManagerBase):
    """
    Базовый менеджер для работы с доступами к фрагментам урока
    """

    def set_trial(self, lesson_fragment: LessonFragment, **kwargs):
        self.set_access(lesson_fragment=lesson_fragment, **kwargs)

    def set_available_access(self, user: User, second_fragment: LessonFragment) -> models.Model:
        return self.objects.set_access(
            status=self.COURSES_STATUS_AVAILABLE,
            lesson_fragment=second_fragment,
            user=user,
        )


class LessonFragmentAccess(AccessBase):
    lesson_fragment = models.ForeignKey(LessonFragment, on_delete=models.CASCADE)
    objects = LessonFragmentAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к фрагменту урока'
        verbose_name_plural = 'Доступ к фрагментам урока'
