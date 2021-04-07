from rest_framework import exceptions
from rest_framework.permissions import BasePermission

from courses_access.models import LessonFragmentAccess


class LessonFragmentAccessPermissions(BasePermission):
    def has_permission(self, request, view, addition: dict = None) -> bool:
        """
        Базовый класс на проверку доступов к моделям из courses-app
        """
        kwargs = view.__dict__.get('kwargs') or {}

        pk = kwargs.get('pk')
        is_accessible = LessonFragmentAccess.objects.is_accessible(user=request.user, lesson_fragment_id=pk)  # TODO провертчь, что доступ не блокированный
        if not is_accessible and pk:
            raise exceptions.NotFound('У вас нет доступа к фрагменту урока')
        return True
