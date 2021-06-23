import typing as t
from django.utils import timezone

from courses_access.utils.general import force_int_pk, to_snake_case


def struct_to_object(**kwargs) -> object:
    """
    Метод генерирует структуру с необходимымми атрибутами
    :param kwargs: Атрибуты
    :return: AccessSimple
    """
    return type('AccessSimple', (), kwargs)


def simple_struct(pk: int, status: t.Optional[int], **kwargs) -> dict:
    """
    Метод возвращает пустую структкру для записи модели доступа
    :param pk: ID модели
    :param status: Статус доступа
    """
    return {
        'pk': pk,
        'status': status,
        'date_updated': timezone.now(),
        'date_completed': None,
        **kwargs,
    }


@force_int_pk
def get_object(access, to_struct: str, pk: int):  # TODO: Удалить дубликат в толстой модели Access
    """
    Метод возвращает объект одной стуркутуры данных:
        - Course
        - CourseTheme
        - CourseLesson
        - LessonFragment
    :param access: Объект доступа
    :param to_struct: Название структуры
    :param pk: Уникальный id целевой структуры
    :return: Словарь, представленный объектом
    """
    to_struct = to_snake_case(to_struct)

    if to_struct == 'course':
        return access

    for item in getattr(access, to_struct, []):
        if item['pk'] == pk:
            return struct_to_object(**item)
    return None
