from django.db import models
from users.models import User
from markdownx.models import MarkdownxField


class Dialog(models.Model):
    users = models.ManyToManyField(
        User,
        verbose_name='Пользователи',
        blank=True,
        related_name="dialog_users_set",
        related_query_name="dialog_users",
    )

    date_created = models.DateTimeField('Дата создания', auto_now=True)

    @property
    def websocket_key(self) -> str:
        return 'dialog__%s' % self.id


class DialogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)

    body = MarkdownxField('Сообщение', null=True, blank=True)
    date_created = models.DateTimeField('Дата отправления', auto_now_add=True)
    date_read = models.DateTimeField('Дата прочтения', null=True, blank=True)

    class Meta:
        ordering = ('-date_created', )
