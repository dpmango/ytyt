from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from courses.models import CourseLesson
from courses.utils import html_to_text
from files.models import File
from users.models import User


class Dialog(models.Model):

    date_created = models.DateTimeField('Дата создания', auto_now=True)
    users = models.ManyToManyField(
        User,
        verbose_name='Пользователи',
        blank=True,
        related_name="dialog_users_set",
        related_query_name="dialog_users",
    )


class DialogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(CourseLesson, on_delete=models.SET_NULL, null=True, blank=True)

    body = MarkdownxField('Сообщение', null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField('Дата отправления', auto_now_add=True)
    date_read = models.DateTimeField('Дата прочтения', null=True, blank=True)

    class Meta:
        ordering = ('date_created', )

    def get_body(self) -> str:
        return markdownify(self.body)

    def get_text_body(self) -> str:
        return html_to_text(self.get_body())
