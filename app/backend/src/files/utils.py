import typing as t
from urllib.parse import urljoin

from django.core.files import File
from django.utils import timezone
from sorl.thumbnail import get_thumbnail


def upload_path(instance, filename):
    return '%s/%s/%s' % (timezone.now().strftime('%Y/%m'), instance.user.id, filename)


def generate_thumb_url(content: File, base_url: str, size: str, quality: int = None) -> t.Optional[str]:
    if content:
        thumb = get_thumbnail(content, size, crop='center', quality=quality or 99)
        return urljoin(base_url, thumb.url)
    return None
