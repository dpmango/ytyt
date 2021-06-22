from django.conf import settings

from courses_access.models import Access
from crm.celery import app


def update_users_access() -> None:
    """
    Функция-оберетка для вызова асинхронной функции обновления
    """
    if settings.IS_PRODUCTION:
        task_update_users_access.delay()
    else:
        task_update_users_access()


@app.task(bind=True)
def task_update_users_access(_, *args, **kwargs) -> None:
    """
    Метод обновляет доступы ко всем зависимым структурам данных
    :param _: Объект celery
    :param args: Аргументы вызова
    :param kwargs: Ключевые аргументы вызова
    """
    for access in Access.objects.all():
        access.update_access_structs()
