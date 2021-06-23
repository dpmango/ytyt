import typing as t

from django.utils import timezone

from courses.models import CourseTheme, CourseLesson, LessonFragment
from courses_access.core.base import simple_struct, get_object
from courses_access.models import Access
from courses_access.utils.general import to_snake_case
from loguru import logger


def update_structs_sorting(access: Access, created: bool = None) -> None:
    """
    Функция обновляет порядок следования всех структур: Темы, уроки, фрагменты
    В зависимости от нового порядка следования будут актуализированы статусы
    :param access: Модель доступа
    :param created: Вызов фнукции произошел как следствие создания нового элемента или нет
    """
    queryset_course_themes = access.queryset_themes()

    course_lessons = []
    lesson_fragments = []
    course_themes = _update_struct(
        access, to_struct='course_theme', data=queryset_course_themes
    )

    for _theme in queryset_course_themes.order_by('order'):
        _course_lessons = _theme.courselesson_set.all().order_by('order')
        course_lessons.extend(
            _update_struct(
                access, to_struct='course_lesson', data=_course_lessons,
            )
        )

        for _course_lesson in _course_lessons:
            _lesson_fragments = _course_lesson.lessonfragment_set.all().order_by('id')

            lesson_fragments.extend(
                _update_struct(
                    access, to_struct='lesson_fragment', data=_lesson_fragments,
                )
            )

    if not created:
        logger.debug('[Update structs statuses] access_id=%s, access=%s, created=%s' % (access.id, access, created))

        course_themes = _update_struct_statuses(access, course_themes)
        course_lessons = _update_struct_statuses(access, course_lessons)
        lesson_fragments = _update_struct_statuses(access, lesson_fragments)

    access.course_theme = course_themes
    access.course_lesson = course_lessons
    access.lesson_fragment = lesson_fragments

    access.save(update_fields=['course_theme', 'course_lesson', 'lesson_fragment', 'date_updated'])


def _update_struct(
        access: Access,
        to_struct: str,
        data: t.List[t.Union[CourseTheme, CourseLesson, LessonFragment]]
) -> t.List[dict]:
    """
    Функция обновляет порядок структуры. Если были добавлены новые элементы, то добавляет их к общей структуре
    :param access: Модель доступа
    :param to_struct: Название структуры, с которой происходит работа
    :param data: Данные для обновления
    """

    _extension_funcs_mapping = {
        'course_theme': lambda theme: dict(
            free_access=theme.free_access, pk=theme.pk,
        ),
        'course_lesson': lambda course_lesson: dict(
            course_theme_id=course_lesson.course_theme.pk, pk=course_lesson.pk,
        ),
        'lesson_fragment': lambda lesson_fragment: dict(
            course_theme_id=lesson_fragment.course_lesson.course_theme.pk,
            course_lesson_id=lesson_fragment.course_lesson.pk,
            pk=lesson_fragment.pk,
        ),
    }

    to_struct = to_snake_case(to_struct)
    extension_func = _extension_funcs_mapping.get(to_struct)
    extension_result = []

    for item_struct in data:
        object_old_struct = get_object(access, to_struct, pk=item_struct.pk)

        if object_old_struct:
            # Если структура ранее ожидалась на корректировку, то переводим ее немедленную корректировку, а
            # ожидание корректировки удаляем
            kwargs_statuses = dict(status=object_old_struct.status)
        else:
            kwargs_statuses = dict(status=None)

        extension_result.append(
            simple_struct(
                **extension_func(item_struct), **kwargs_statuses,
            )
        )

    return extension_result


def _update_struct_statuses(access, data: t.List[dict]) -> list:
    """
    Метод обновляет статусы для новых, ранее неизвестных, элементов структуры
    :param access: Модель доступа
    :param data: Данные для обновления статусов
    """
    # Если курс завершен, то нет смысла что-то проверять, просто открываем доступ к новым/обновленным структурам
    if access.status == Access.STATUS_COMPLETED:
        return [{**item, 'status': Access.STATUS_AVAILABLE} for item in data]

    # Отдаем приоритет первому уроку в прогрессе
    control_index = None
    for idx, item in enumerate(data):
        if item['status'] == Access.STATUS_IN_PROGRESS:
            control_index = idx

    # Если уроков в прогрессе нет, то ищем последний доступный
    if control_index is None:
        for idx, item in enumerate(data):
            if item['status'] == Access.STATUS_AVAILABLE:
                control_index = idx

    # Если последнего доступного нет, то ищем последний завершенный (Такого случить не должно, но все-таки)
    if control_index is None:
        for idx, item in enumerate(data):
            if item['status'] == Access.STATUS_COMPLETED:
                control_index = idx

    updated_struct = []
    target_status = Access.STATUS_AVAILABLE

    # Если самый первый элемент структуры без статуса, то делаем его просто доступным
    if control_index == 0:
        status = data[control_index]['status']
        target_status = Access.STATUS_AVAILABLE if status is None else status

    for idx, item in enumerate(data):
        if idx == control_index:
            status = data[control_index]['status']
        else:
            status = Access.STATUS_BLOCK if idx > control_index else target_status

        updated_struct.append({**item, 'status': status, 'date_updated': timezone.now()})

    return updated_struct
