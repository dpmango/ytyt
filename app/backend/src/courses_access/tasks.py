from courses_access.models import Access
from crm.celery import app


def update_user_access(course_id: int) -> None:
    """
    Функция-оберетка для вызова асинхронной функции обновления
    :param course_id: ID курса
    """
    task_update_user_access.delay(course_id=course_id)


@app.task(bind=True)
def task_update_user_access(_, *args, course_id: int = None, **kwargs) -> None:
    """
    Метод обновляет доступы ко всем зависимым структурам данных
    :param _: Объект celery
    :param args: Аргументы вызова
    :param course_id: ID курса для обновления
    :param kwargs: Ключевые аргументы вызова
    """
    if not course_id:
        return None

    for access in Access.objects.filter(course_id=course_id):
        access.update_structs()
