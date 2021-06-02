import rest_framework.permissions as perm
from rest_framework import exceptions

from courses.models import Course, CourseTheme, CourseLesson, LessonFragment
from courses_access.models import Access


class IsInStuffGroups(perm.BasePermission):
    def has_permission(self, request, view) -> bool:
        """
        Метод проверяет наличие пользователя в одной из доверенных групп
        is_staff=True у пользователя НЕ является обязательным
        :param request: Объект запроса
        :param view: Вьюха соответсвующая запросу
        """
        user = request.user
        is_authenticated = bool(user and user.is_authenticated)

        if not is_authenticated:
            raise exceptions.PermissionDenied('Для доступа необходимо быть авторизованным')

        if user and user.in_stuff_groups:
            return True

        return False


class CourseThemeAccessPermissions(perm.BasePermission):
    def has_permission(self, request, view) -> bool:
        """
        Проверка доступа юзера к теме
        Этапы проверки:
            1. Проверка на суперюзера/админа
            2. Наличие авторизации юзера
            3. Проверка доступа к курсу
            4. Проверка доступа к теме курса
        :param request: Объект запроса
        :param view: Вьюха соответсвующая запросу
        """
        user = request.user
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
        course_theme_manual = access.check_manual_access('course_theme', course_theme_id)

        # Если нет обычного доступа к теме курса и нет ручного доступа к теме курса, то вернем ошибку
        if not course_theme_permission and not course_theme_manual:

            detail = 'У вас нет доступа к теме `%s`' % CourseTheme.objects.get(pk=course_theme_id).title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})
        return True


class CourseLessonAccessPermissions(CourseThemeAccessPermissions):
    def has_permission(self, request, view) -> bool:
        """
        Проверка доступа юзера к уроку
        Этапы проверки:
            1-4. Проверки из класса `CourseThemeAccessPermissions`
            5. Проверка доступа к уроку
        :param request: Объект запроса
        :param view: Вьюха соответсвующая запросу
        """
        super().has_permission(request, view)
        user = request.user

        course_id = view.kwargs.get('course_id')
        access = Access.objects.filter(course_id=course_id, user=user).first()

        course_lesson_id = view.kwargs.get('pk')
        course_lesson_permission = access.check_course_lesson_permission(pk=course_lesson_id)
        course_lesson_manual = access.check_manual_access('course_lesson', course_lesson_id)

        # Если нет обычного доступа к уроку и нет ручного доступа к уроку, то вернем ошибку
        if not course_lesson_permission and not course_lesson_manual:

            detail = 'У вас нет доступа к уроку `%s`' % CourseLesson.objects.get(pk=course_lesson_id).title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})
        return True


class LessonFragmentAccessPermissions(CourseLessonAccessPermissions):
    def has_permission(self, request, view) -> bool:
        """
        Проверка доступа юзера к фрагменту урока
        Этапы проверки:
            1-5. Проверки из класса `CourseLessonAccessPermissions`
            6. Проверка доступа к фрагменту
        :param request: Объект запроса
        :param view: Вьюха соответсвующая запросу
        :return:
        """
        user = request.user
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
        lesson_fragment_permission = access.check_lesson_fragment_permission(pk=lesson_fragment_id)
        course_lesson_manual = access.check_manual_access('lesson_fragment', lesson_fragment_id)

        # Если нет объекта доступа или нет обычного доступа или ручного доступа к фрагменту, то вернем ошибку
        if not access or (not lesson_fragment_permission and not course_lesson_manual):
            detail = 'У вас нет доступа к фрагменту `%s`' % lesson_fragment.title
            raise exceptions.PermissionDenied({'detail': detail, **access.get_block_reason()})
        return True
