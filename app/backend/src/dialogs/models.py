from bs4 import BeautifulSoup
from django.db import models
from markdownx.models import MarkdownxField

from courses.models import CourseLesson
from files.models import File
from users.models import User
from markdownx.utils import markdownify


class Dialog(models.Model):

    date_created = models.DateTimeField('Дата создания', auto_now=True)
    users = models.ManyToManyField(
        User,
        verbose_name='Пользователи',
        blank=True,
        related_name="dialog_users_set",
        related_query_name="dialog_users",
    )

    @property
    def ws_key(self) -> str:
        return 'dialog__%s' % self.id


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

    def get_body(self):
        return markdownify(self.body)

    def get_text_body(self):
        return ''.join(BeautifulSoup(self.get_body(), features='html.parser').findAll(text=True))
