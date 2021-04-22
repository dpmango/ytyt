from django.db import models
from django.utils.translation import gettext_lazy as _


class ReviewersMixins(models.Model):
    """
    Миксин-класс для работы с пользователем, как с ревьюером
    """

    reviewer = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True
