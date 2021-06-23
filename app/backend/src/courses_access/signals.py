import typing as t
from datetime import datetime, timedelta

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from loguru import logger

from courses import models
from courses_access.tasks import update_users_access


def __update_access(signal_name: str, sender: t.Union[models.CourseTheme, models.CourseLesson], created: bool = None):

    # prefix__{signal-name}
    key = 'update_access__%s' % signal_name

    last_update = cache.get(key)
    now = datetime.now().timestamp()

    # Обновляем только в том случае, если с последнего обновления прошло 3 секунду (Число может быть любым)
    # Если сделать обновление на каждом событии сингала, то стуркута обновится столько раз, сколько
    # было объектов изменено
    if not last_update or now - last_update > timedelta(seconds=3).seconds:
        logger.debug(
            '[Init update structs] signal_name=%s, sender=%s, created=%s' % (
                signal_name, sender, created
            )
        )

        update_users_access(created=created)
        cache.set(key, now)


@receiver(post_save, sender=models.CourseTheme)
def update_access_theme_save(sender, instance, *args, created: bool = None, **kwargs):
    __update_access('post_save', sender, created=created)


@receiver(post_save, sender=models.CourseLesson)
def update_access_lesson_save(sender, instance, *args, created: bool = None, **kwargs):
    __update_access('post_save', sender, created=created)


@receiver(post_delete, sender=models.CourseTheme)
def update_access_theme_delete(sender, instance, *args, **kwargs):
    __update_access('post_delete', sender)


@receiver(post_delete, sender=models.CourseLesson)
def update_access_lesson_delete(sender, instance, *args, **kwargs):
    __update_access('post_delete', sender)


@receiver(post_delete, sender=models.LessonFragment)
def update_access_lesson_fragment_delete(sender, instance, *args, **kwargs):
    __update_access('post_delete', sender)
