from django.conf import settings

from courses_access.core.struct import sorting as struct_sorting
from courses_access.models import Access
from crm.celery import app


def update_users_access(created: bool = None) -> None:
    """
    Функция-оберетка для вызова асинхронной функции обновления
    :param created: Была ли создана модель
    """
    if settings.IS_PRODUCTION:
        task_update_users_access.delay(created=created)
    else:
        task_update_users_access(created=created)


@app.task(bind=True, soft_time_limit=3)
def task_update_users_access(_, *args, created: bool = None, **kwargs) -> None:
    """
    Метод обновляет доступы ко всем зависимым структурам данных
    :param _: Объект celery
    :param created: Была ли создана модель
    :param args: Аргументы вызова
    :param kwargs: Ключевые аргументы вызова
    """
    for access in Access.objects.all():
        struct_sorting.update_structs_sorting(access, created=created)
