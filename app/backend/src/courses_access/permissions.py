import rest_framework.permissions as perm
from rest_framework import exceptions

from courses.models import Course, CourseTheme, CourseLesson, LessonFragment
from courses_access.models import Access


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
        access = Access.objects.filter(course_id=course_id, user=user).first()

        if not access or not access.check_course_permission():

            detail = 'У вас нет доступа к курсу `%s`' % Course.objects.get(pk=course_id).title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})

        course_theme_id = view.kwargs.get('course_theme_id')
        course_theme_permission = access.check_course_theme_permission(pk=course_theme_id)
        if not course_theme_permission:

            detail = 'У вас нет доступа к теме `%s`' % CourseTheme.objects.get(pk=course_theme_id).title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})

        course_lesson_id = view.kwargs.get('pk')
        course_lesson_permission = access.check_course_lesson_permission(pk=course_lesson_id)
        if not course_lesson_permission:

            detail = 'У вас нет доступа к уроку `%s`' % CourseLesson.objects.get(pk=course_lesson_id).title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})

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

        access = Access.objects.filter(course=course, user=user).first()
        if not access or not access.check_lesson_fragment_permission(pk=lesson_fragment_id):
            detail = 'У вас нет доступа к фрагменту `%s`' % lesson_fragment.title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})
        return True
