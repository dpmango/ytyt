from django.db import models

from files.utils import upload_path
from users.models import User


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    content = models.FileField('Файл', upload_to=upload_path)
