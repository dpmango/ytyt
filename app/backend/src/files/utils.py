import os
import typing as t
from urllib.parse import urljoin

from django.conf import settings
from django.core.files import File
from django.utils import timezone
from sorl.thumbnail import get_thumbnail


def upload_path(instance, filename):
    return '%s/%s/%s' % (timezone.now().strftime('%Y/%m'), instance.user.id, filename)


def upload_course_path(instance, filename):
    return '%s/%s' % (settings.MARKDOWNX_MEDIA_PATH.lstrip('/'), filename)


def generate_thumb_url(content: File, base_url: str, size: str, quality: int = None) -> t.Optional[str]:
    """
    Функция генерирует ссылку миниатюру для изображения
    :param content: Изображение
    :param base_url: Базовый путь backend сервиса
    :param size: Размеры формата 100x100
    :param quality: Качество изображения
    """
    _, file_name = os.path.split(content.name)
    format_ = 'PNG' if os.path.splitext(file_name)[1] == '.png' else 'JPEG'

    if content:
        thumb = get_thumbnail(
            content, size, crop='center', quality=quality or 100, format=format_
        )
        return urljoin(base_url, thumb.url)
    return None
