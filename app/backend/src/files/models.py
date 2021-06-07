import typing as t
from urllib.parse import urljoin

from django.db import models

from files.utils import upload_path
from users.models import User


class File(models.Model):

    TYPE_FILE = 1
    TYPE_IMAGE = 2
    TYPE_UNKNOWN = 3
    TYPES = (
        (TYPE_FILE, 'Файл'),
        (TYPE_IMAGE, 'Изображение'),
        (TYPE_UNKNOWN, 'Остальное'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    content = models.FileField('Файл', upload_to=upload_path)
    type = models.PositiveIntegerField('Тип файла', choices=TYPES, default=TYPE_UNKNOWN)
    file_name = models.CharField('Название файла', null=True, blank=True, max_length=250)

    def generate_url(self, base_url: str) -> t.Optional[str]:
        if self.content:
            return urljoin(base_url, self.content.url)
        return None
