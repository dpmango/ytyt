import typing as t
from urllib.parse import urljoin

from django.core.files.images import ImageFile
from django.db import models

from files.utils import upload_path, upload_course_path
from users.models import User


class File(models.Model):

    TYPE_FILE = 1
    TYPE_IMAGE = 2
    TYPES = (
        (TYPE_FILE, 'Файл'),
        (TYPE_IMAGE, 'Изображение'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    content = models.FileField('Файл', upload_to=upload_path)
    type = models.PositiveIntegerField('Тип файла', choices=TYPES, default=TYPE_FILE)
    file_name = models.CharField('Название файла', null=True, blank=True, max_length=250)

    def generate_url(self, base_url: str) -> t.Optional[str]:
        if self.content:
            return urljoin(base_url, self.content.url)
        return None

    @property
    def width(self) -> t.Optional[int]:
        if self.type == self.TYPE_IMAGE:
            return ImageFile(self.content.file).width
        return None

    @property
    def height(self) -> t.Optional[int]:
        if self.type == self.TYPE_IMAGE:
            return ImageFile(self.content.file).height
        return None


class CourseFile(models.Model):
    content = models.FileField('Файл', upload_to=upload_course_path)

    def generate_url(self, base_url: str) -> t.Optional[str]:
        if self.content:
            return urljoin(base_url, self.content.url)
        return None
