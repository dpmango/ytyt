from datetime import datetime, timedelta

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from courses import models
from courses_access.tasks import update_users_access


def __update_access():
    key = 'last_update_access'
    last_update = cache.get('last_update_access')
    now = datetime.now().timestamp()

    # Обновляем только в том случае, если с последнего обновления прошло 7 секунду (Число может быть любым)
    # Если сделать обновление на каждом событии сингала, то стуркута обновится столько раз, сколько
    # было объектов изменено
    if not last_update or now - last_update > timedelta(seconds=7).seconds:
        update_users_access()
        cache.set(key, now)


@receiver([post_save, post_delete], sender=models.CourseTheme)
def update_access_theme(sender, instance, *args, **kwargs):
    __update_access()


@receiver([post_save, post_delete], sender=models.CourseLesson)
def update_access_lesson(sender, instance, *args, **kwargs):
    __update_access()
