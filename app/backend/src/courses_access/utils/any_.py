import typing
from courses.models import *


def force_int_pk(func):
    def wrapper(*args, **kwargs):
        if 'pk' in kwargs:
            kwargs['pk'] = int(kwargs['pk'])

        return func(*args, **kwargs)

    return wrapper


def to_snake_case(string: str) -> str:
    """
    Example: CourseTheme —> course_theme
    :param string: Любой текст
    :return: Текст в формате snake_case
    """
    snake_string = ''
    for id_, char in enumerate(string):
        if char.isupper() and id_ != 0:
            snake_string += '_'

        snake_string += char.lower()
    return snake_string


def get_course_from_struct(obj) -> typing.Optional[int]:
    """
    Метод возвращает id курса по входящей структуре
    :param obj: Некоторая структура из курсов
    """
    course_id = None

    if isinstance(obj, Course):
        course_id = obj.id

    elif isinstance(obj, CourseTheme):
        course_id = obj.course_id

    elif isinstance(obj, CourseLesson):
        course_id = obj.course_theme.course_id

    elif isinstance(obj, LessonFragment):
        course_id = obj.course_lesson.course_theme.course_id

    return course_id
