"""
Модуль для работы с кэшем в рамках модели доступа к курсам
"""
from django.core.cache import cache


def set_pending_adjustment(to_struct: str, pk: int) -> None:
    """
    Функция сохраняет структуру, которая ожидает корректировки в моделях доступа
    Запись сообщает, что данная сструктура когда-то будет скорректирована
    :param to_struct: Название структуры
    :param pk: ID структуры
    """
    cache.set('pending_adjustment__%s__%s' % (to_struct, pk), 1)


def exists_pending_adjustment(to_struct: str, pk: int) -> bool:
    """
    Функция проверяет наличие структуры, которая ожидает корректировки в моделях доступа
    :param to_struct: Название структуры
    :param pk: ID структуры
    """
    return bool(cache.get('pending_adjustment__%s__%s' % (to_struct, pk)))


def delete_pending_adjustment(to_struct: str, pk: int) -> None:
    """
    Функция удаляет структуру, которая ожидает корректировки в моделях доступа
    :param to_struct: Название структуры
    :param pk: ID структуры
    """
    cache.delete('pending_adjustment__%s__%s' % (to_struct, pk))
