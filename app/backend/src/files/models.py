import os
import typing as t
from urllib.parse import urljoin

from django.db import models

from files.utils import upload_path
from users.models import User


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    content = models.FileField('Файл', upload_to=upload_path)

    def is_image(self) -> bool:
        if self.content:
            if os.path.splitext(self.file_name)[1] in ('.jpg', '.jpeg', '.png', '.svg'):
                return True
        return False

    def url(self, base_url: str) -> t.Optional[str]:
        if self.content:
            return urljoin(base_url, self.content.url)
        return None

    @property
    def file_name(self):
        return os.path.split(self.content.file.name)[1]
