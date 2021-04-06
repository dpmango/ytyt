from rest_framework.permissions import BasePermission
from courses_access.models import CourseAccess, CourseThemeAccess, CourseLessonAccess
from rest_framework import exceptions


class CourseAccessPermissions(BasePermission):
    ACCESSIBLE_ACTIONS = (
        'list',
        'retrieve',
    )

    def has_permission(self, request, view, addition: dict = None) -> bool:
        """
        Базовый класс на проверку доступов к моделям из courses-app
        """
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if not is_authenticated:
            raise exceptions.NotFound('Не найдено')  # TODO: set correct error

        kwargs = view.__dict__.get('kwargs') or {}
        pk = kwargs.get('pk') if not addition or len(addition) == 0 else addition.get('course_id')

        is_accessible = CourseAccess.objects.is_accessible(user=request.user, course_id=pk)
        if not is_accessible and pk:
            raise exceptions.NotFound('У вас нет доступа к курсу')
        return True


class CourseThemeAccessPermissions(CourseAccessPermissions):

    def has_permission(self, request, view, addition: dict = None) -> bool:
        """
        Базовый класс на проверку доступов к моделям из courses-app
        """
        kwargs = view.__dict__.get('kwargs') or {}
        super().has_permission(request, view, addition or kwargs or {})

        pk = kwargs.get('pk') if not addition or len(addition) == 0 else addition.get('course_theme_id')
        is_accessible = CourseThemeAccess.objects.is_accessible(user=request.user, course_theme_id=pk)

        if not is_accessible and pk:
            raise exceptions.NotFound('У вас нет доступа к теме курса')
        return True


class CourseLessonAccessPermissions(CourseThemeAccessPermissions):

    def has_permission(self, request, view, addition: dict = None) -> bool:
        """
        Базовый класс на проверку доступов к моделям из courses-app
        """
        kwargs = view.__dict__.get('kwargs') or {}
        super().has_permission(request, view, kwargs)

        pk = kwargs.get('pk')
        is_accessible = CourseLessonAccess.objects.is_accessible(user=request.user, course_lesson_id=pk)
        if not is_accessible and pk:
            raise exceptions.NotFound('У вас нет доступа к уроку')
        return True

