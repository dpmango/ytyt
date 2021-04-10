from rest_framework import exceptions

import rest_framework.permissions as perm


from courses_access.models import CourseAccess, CourseThemeAccess, CourseLessonAccess, LessonFragmentAccess
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


class CourseLessonAccessPermissions(perm.BasePermission):
    
    def has_permission(self, request, view) -> bool:
        """
        Проверка доступа юзера к уроку
        Этапы проверки:
            1. Проверка на суперюзера/админа
            2. Проверка на детализацию (Если не запрашивают детализацию урока, то все ок)
            3. Наличие авторизации юзера
            4. Проверка доступа к курсу
            5. Проверка доступа к теме курса
            6. Проверка доступа к уроку
        :param request: Объект запроса
        :param view: Вьюха соответсвующая запросу
        """
        user = request.user
        if user and (user.is_staff or user.is_superuser):
            return True

        is_detail = view.detail
        if not is_detail and request.method in perm.SAFE_METHODS:
            return True

        is_authenticated = bool(user and user.is_authenticated)
        if not is_authenticated:
            raise exceptions.PermissionDenied('Для доступа необходимо быть авторизованным')

        course_id = view.kwargs.get('course_id')
        course_permission = CourseAccess.objects.check_permission(course_id, user)
        if not course_permission:
            raise exceptions.PermissionDenied(
                'У вас нет доступа к курсу `%s`' % Course.objects.get(pk=course_id).title
            )

        course_theme_id = view.kwargs.get('course_theme_id')
        course_theme_permission = CourseThemeAccess.objects.check_permission(course_theme_id, user)
        if not course_theme_permission:
            raise exceptions.PermissionDenied(
                'У вас нет доступа к теме `%s`' % CourseTheme.objects.get(pk=course_theme_id).title
            )

        course_lesson_id = view.kwargs.get('pk')
        course_lesson_permission = CourseLessonAccess.objects.check_permission(course_lesson_id, user)
        if not course_lesson_permission:
            raise exceptions.PermissionDenied(
                'У вас нет доступа к уроку `%s`' % CourseLesson.objects.get(pk=course_lesson_id).title
            )

        return True


class LessonFragmentAccessPermissions(CourseLessonAccessPermissions):

    def has_permission(self, request, view) -> bool:
        """
        Проверка доступа юзера к фрагменту урока
        Этапы проверки:
            1-6. Проверки из класса `CourseLessonAccessPermissions`
            7. Проверка доступа к фрагменту
        :param request: Объект запроса
        :param view: Вьюха соответсвующая запросу
        :return:
        """
        user = request.user
        if user and (user.is_staff or user.is_superuser):
            return True

        lesson_fragment_id = view.kwargs.get('pk')

        lesson_fragment = LessonFragment.objects.get(pk=lesson_fragment_id)
        course_lesson = lesson_fragment.course_lesson
        course_theme = course_lesson.course_theme
        course = course_theme.course

        ini_kwargs = view.kwargs.copy()
        view.kwargs = {
            'course_id': course_theme.course.id,
            'course_theme_id': course_theme.id,
            'pk': course_lesson.id
        }

        # Вызывам необходимые проверки существующих моделей
        super().has_permission(request, view)
        view.kwargs = ini_kwargs

        lesson_fragment_permission = LessonFragmentAccess.objects.check_permission(
            lesson_fragment_id, request.user, course=course, course_theme=course_theme
        )
        if not lesson_fragment_permission:
            raise exceptions.PermissionDenied('У вас нет доступа к фрагменту `%s`' % lesson_fragment.title)
        return True
